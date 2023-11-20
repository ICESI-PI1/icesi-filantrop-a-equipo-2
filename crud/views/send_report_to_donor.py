from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from crud.models import *
from crud.models import Document as AcademicDocument
from datetime import datetime
from docx import Document
from docx.shared import Pt
import traceback

from crud.views.request_info_update import send_email


"""
Renders the page to generate and send reports to donors. 

Also, once the user has typed all required information, gets that info and calls the different functions to generate and display the report on page.
"""
@login_required
def send_report_to_donor(request):
    if request.method == 'POST':
        # Dictionary to save the info that will be charged to the html with the generated report.
        html_data = {}

        try:
            # Get the info to generate the report and send the email
            selected_donor_id = request.POST.get('donor-id', '')

            selected_student_id = request.POST.get('student-id', '')

            if selected_donor_id == '' or selected_student_id == '':
                raise ValueError('Error. Seleccione un donante y un estudiante')
                
            email_message = request.POST.get('message-area', '')

            # Charges the info to the dictionary to charge it again with the report
            html_data['selected_donor_id'] = selected_donor_id
            html_data['email_message'] = email_message
            
            student_testimony = request.POST.get('student-testimony', '')

            date = datetime.now().date()
            semester = f'{date.year} - 1' if date.month < 6 else f'{date.year} - 2'

            report_type = request.POST.get('report-type', '')

            # Tries to get the selected student's non academic activities. If there is no one, don't stop the report generation. 
            try:
                non_academic_activities = NonAcademicActvitiesReport.objects.get(student_code=selected_student_id)

            except Exception as e:
                traceback.print_exc()
                print(f"Error: {e}")

                non_academic_activities = "No se registran asistencias a actividades no académicas."

            try:
                crea_assistance = CREAReport.objects.get(student_code=selected_student_id)

            except Exception as e:
                traceback.print_exc()
                print(f"Error: {e}")

                crea_assistance = "No se registran asistencias a monitorías."

            try:
                academic_info = AcademicDocument.objects.filter(codigo_estudiante=selected_student_id).first()

                academic_report_name = str(academic_info.uploadedFile).split('/')[-1]
                print(academic_report_name)

                # Charges the academic report name if there is a matching document
                html_data['academic_report_name'] = academic_report_name

            # Catches the exception when there is not a matching document
            except Exception as e:
                traceback.print_exc()
                print(f"Error: {e}")

                academic_info = None
                academic_report_name = None

            report_name = ''

            # Searches the selected student on the db
            selected_student = Student.objects.get(id=selected_student_id)

            # Send different parameters depending on the report type
            if 'Reporte general' in report_type:
                if  academic_info is None:
                    academic_info = 'No se registra información académica.'

                    report_name = generate_report(date, semester, selected_student, report_type, testimony=student_testimony, non_academic_activities=non_academic_activities, crea_assistance=crea_assistance, academic_info=academic_info)
                else:
                    report_name = generate_report(date, semester, selected_student, report_type, testimony=student_testimony, non_academic_activities=non_academic_activities, crea_assistance=crea_assistance)

            elif 'Reporte de actividades no académicas' in report_type:
                report_name = generate_report(date, semester, selected_student, report_type, non_academic_activities=non_academic_activities)

            elif 'Reporte de asistencia al CREA' in report_type:
                report_name = generate_report(date, semester, selected_student, report_type, crea_assistance=crea_assistance)
                print(crea_assistance)

            result_message = "Reporte generado con éxito"

            # Charges the generated report name to the html once it has been created successfully
            html_data['generated_report'] = report_name

        # Catches if there is a problem in the generation of the report
        except ValueError as ve:
            result_message = str(ve)

        except Exception as e:
            traceback.print_exc()
            print(f"Error: {e}")

            report_name = None
            result_message = "Error en la generación de reporte"
        
        # Charges the operation's result message to notice the user about it
        html_data['result_message'] = result_message

        return render(request, 'send_report_to_donor.html', html_data)

    return render(request, 'send_report_to_donor.html')


"""
Manages the event when the user clicks the send button, confirming that she/he is in agreement by sending the generated report.
"""
@login_required
def send_report(request):
    try:
        # Gets the info
        selected_donor_id = request.POST.get('donor-id2', '')
        selected_donor = Donor.objects.get(id=selected_donor_id)

        email_message = request.POST.get('email-message', '')
        
        # Array of document paths to send in the email
        attachment_paths = []

        generated_report_name = request.POST.get('report-name', '')
        report_path = f'crud/static/reports/{generated_report_name}'
        
        # Appends the path of the report
        attachment_paths.append(report_path)

        academic_report_name = request.POST.get('academic-report-name', '')

        # Checks if the academic_report_name is present and appends its path to the array if it is
        if academic_report_name:
            academic_report_path = f'media/Uploaded Files/{academic_report_name}'
            attachment_paths.append(academic_report_path)

        # This is a generic subject for the email. It can be changed
        subject = 'Reporte general de beneficiario'

        # Sends the email by using the function send_email() on reques_info_update.py
        send_email(selected_donor.email, email_message, subject, attachment_paths=attachment_paths)

        return redirect('/sendReportToDonor/')

    # Notices the user if something went wrong
    except Exception as e:
        traceback.print_exc()
        print(f'Error: {e}')

        result_message = 'Error al enviar email al donante'

        return render(request, 'send_report_to_donor.html', {
            'email_sending_result_message': result_message,
            "generated_report": generated_report_name,
            "selected_donor_id": selected_donor_id,
            "email_message": email_message,
        })


"""
Receives certain information, obtains the basic format of the report (depending on the value of report_type parameter), and fills in the available fields with the information received.

At the final, returns the name of the generated report.
"""
def generate_report(date, semester, student, report_type, testimony=None, non_academic_activities=None, crea_assistance=None, academic_info=None):
    try:
        report_name = f'{report_type} {student.student_code} - {semester}.docx'
        output_path = f'crud/static/reports/{report_name}'

        # Reads the format content
        format_content = read_report_format(report_type)

        # Creates a new doc to add the modifications
        modified_doc = Document()

        for paragraph_info in format_content:
            new_paragraph = modified_doc.add_paragraph()

            # Replaces the fields with the information received as parameters
            paragraph_text = paragraph_info['paragraph_text']
            paragraph_text = paragraph_text.replace("[Fecha]", str(date))
            paragraph_text = paragraph_text.replace("[estudiante]", str(student.name))
            paragraph_text = paragraph_text.replace("[semestre]", semester)

            if 'Reporte general' in report_type:
                paragraph_text = paragraph_text.replace("[testimonio_estudiante]", testimony)
                paragraph_text = paragraph_text.replace("[actividades_no_académicas]", str(non_academic_activities))
                paragraph_text = paragraph_text.replace("[asistencia_monitorias]", str(crea_assistance))

                # If academic_info is None, removes the field available to this purpose. Otherwise, fills that field
                if academic_info is not None:
                    paragraph_text = paragraph_text.replace("[info_academica]", str(academic_info))
                
                else:
                    paragraph_text = paragraph_text.replace("[info_academica]", '')

            elif 'Reporte de actividades no académicas' in report_type:
                paragraph_text = paragraph_text.replace("[actividades_no_académicas]", str(non_academic_activities))

            elif 'Reporte de asistencia al CREA' in report_type:
                paragraph_text = paragraph_text.replace("[asistencia_monitorias]", str(crea_assistance))

            # Adds the modified text to the doc
            new_paragraph.add_run(paragraph_text)

            for run in new_paragraph.runs:
                for run_info in paragraph_info['runs']:
                    run.font.size = Pt(run_info['font_size']) if run_info['font_size'] else None
                    run.font.bold = run_info['font_bold']
                    run.font.italic = run_info['font_italic']
                    run.font.name = run_info['font_name']
                    new_paragraph.alignment = run_info['alignment']

        # Saves the .docx and .pdf of the report
        modified_doc.save(output_path)

        return output_path.split('/')[-1]

    except Exception as e:
        traceback.print_exc()
        print(f'Error por acá: {e}')



"""
Reads a .docx document containing the basic format of the report to be generated. 
"""
def read_report_format(report_type):
    # Checks the type of the report and reads the corresponding base
    if 'Reporte general' in report_type:
        doc = Document('./crud/static/formats/Reporte general beneficiario.docx')

    elif 'Reporte de actividades no académicas' in report_type:
        doc = Document('./crud/static/formats/Reporte de actividades no académicas beneficiario.docx')

    elif 'Reporte de asistencia al CREA' in report_type:
        doc = Document('./crud/static/formats/Reporte de asistencia al CREA beneficiario.docx')

    doc_content = []

    # Builds a new document with the same text of the base format read
    for paragraph in doc.paragraphs:
        para_content = []

        for run in paragraph.runs:
            run_text = run.text
            font_size = run.font.size.pt if run.font.size else None
            font_bold = run.font.bold
            font_italic = run.font.italic
            paragraph_alignment = paragraph.alignment
            font_name = run.font.name

            # Text styles
            para_content.append({
                'text': run_text,
                'font_size': font_size,
                'font_bold': font_bold,
                'font_italic': font_italic,
                'alignment': paragraph_alignment,
                'font_name': font_name,
            })

        doc_content.append({
            'paragraph_text': paragraph.text,
            'runs': para_content,
        })

    return doc_content
