from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from crud.models import *
from django.http import JsonResponse
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from django.core.files.storage import FileSystemStorage
from django.conf import settings  # Importa la configuración de Django
from datetime import datetime
from docx import Document
from docx.shared import Pt
from docx2pdf import convert
import pythoncom
import os

from crud.views.request_info_update import send_email


@login_required
def send_report_to_donor(request):
    if request.method == 'POST':
        try:
            selected_donor_id = request.POST.get('donor-id', '')

            selected_student_id = request.POST.get('student-id', '')
            selected_student = Student.objects.get(id=selected_student_id)

            email_message = request.POST.get('message-area', '')

            student_testimony = request.POST.get('student-testimony', '')

            date = datetime.now().date()
            semester = f'{date.year} - 1' if date.month < 6 else f'{date.year} - 2'

            report_type = request.POST.get('report-type', '')

            # Tries to get the selected student's non academic activities. If there is no one, don't stop the report generation. 
            try:
                non_academic_activities = NonAcademicActvitiesReport.objects.get(student_code=selected_student_id)

            except Exception as e:
                print(f"Error: {e}")

                non_academic_activities = "No se registran asistencias a actividades no académicas."

            try:
                crea_assistance = CREAReport.objects.get(student_code=selected_student_id)
            
            except Exception as e:
                print(f"Error: {e}")

                crea_assistance = "No se registran asistencias a monitorías."

            report_name = ''

            if 'Reporte general' in report_type:
                report_name = generate_report(date, semester, selected_student, report_type, testimony=student_testimony, non_academic_activities=non_academic_activities, crea_assistance=crea_assistance)

            elif 'Reporte de actividades no académicas' in report_type:
                report_name = generate_report(date, semester, selected_student, report_type, non_academic_activities=non_academic_activities)

            result_message = "Reporte generado con éxito"
            
        except Exception as e:
            print(f"Error: {e}")

            report_name = None
            result_message = "Error en la generación de reporte"
        
        return render(request, 'send_report_to_donor.html', {
            "result_message" : result_message,
            "generated_report" : report_name,
            "selected_donor_id" : selected_donor_id,
            "email_message" : email_message,
        })


    return render(request, 'send_report_to_donor.html')


"""
Manages the event when the user clicks the send button, confirming that she/he is in agreement by sending the generated report.
"""
@login_required
def send_report(request):
    try:
        selected_donor_id = request.POST.get('donor-id2', '')
        selected_donor = Donor.objects.get(id=selected_donor_id)

        email_message = request.POST.get('email-message', '')

        generated_report_name = request.POST.get('report-name', '')
        # report_path = os.path.join(settings.STATIC_ROOT, 'reports', generated_report_name)
        report_path = f'crud/static/reports/{ generated_report_name }'

        subject = 'Reporte general de beneficiario'

        send_email(selected_donor.email, email_message, subject, attachment_path=report_path)

        return redirect('/sendReportToDonor/')

    except Exception as e:
        print(f'Error: {e}')

        result_message = 'Error al enviar email al donante'

        return render(request, 'send_report_to_donor.html', {
            'email_sending_result_message': result_message,
            "generated_report" : generated_report_name,
            "selected_donor_id" : selected_donor_id,
            "email_message" : email_message,
        })


"""
Receives certain information, obtains the basic format of the report (depending on the value of report_type parameter), and fills in the available fields with the information received.

At the final, returns the name of the generated report.
"""
def generate_report(date, semester, student, report_type, testimony=None, non_academic_activities=None, crea_assistance=None):
    try:
        # Calls CoInitialize 'cause there was throwing an exception related with this calling
        pythoncom.CoInitialize()

        report_name = f'{report_type} {student.student_code} - {semester}.docx'
        output_path = f'crud/static/reports/{report_name}'
        output_path_pdf = f'crud/static/reports/{report_name.replace(".docx", ".pdf")}'

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

            elif 'Reporte de actividades no académicas' in report_type:
                paragraph_text = paragraph_text.replace("[actividades_no_académicas]", str(non_academic_activities))


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
        convert(output_path, output_path_pdf)

        return output_path_pdf.split('/')[-1]
    except Exception as e:
        print(f'Error: {e}')

    finally:
        pythoncom.CoUninitialize()



"""
Reads a .docx document containing the basic format of the report to be generated. 
"""
def read_report_format(report_type):
    if 'Reporte general' in report_type:
        doc = Document('./crud/static/formats/Reporte general beneficiario.docx')

    elif 'Reporte de actividades no académicas' in report_type:
        doc = Document('./crud/static/formats/Reporte de actividades no académicas beneficiario.docx')


    doc_content = []

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