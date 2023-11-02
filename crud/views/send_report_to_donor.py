from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from crud.models import *
from django.http import JsonResponse
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from django.core.files.storage import FileSystemStorage
from django.conf import settings  # Importa la configuración de Django
import os
from datetime import datetime
from docx import Document
from docx.shared import Pt
from docx2pdf import convert


@login_required
def send_report_to_donor(request):
    if request.method == 'POST':
        try:
            selected_donor_id = request.POST.get('donor-id', '')
            selected_donor = Donor.objects.get(id=selected_donor_id)

            selected_student_id = request.POST.get('student-id', '')
            selected_student = Student.objects.get(id=selected_student_id)

            email_message = request.POST.get('message-area', '')

            student_testimony = request.POST.get('student-testimony', '')

            date = datetime.now().date()
            semester = f'{date.year} - 1' if date.month < 6 else f'{date.year} - 2'

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

            generate_general_report(date, semester, selected_student, student_testimony, non_academic_activities, crea_assistance)

            # print("Donante: {}".format(selected_donor))
            # print("Estudiante: {}".format(selected_student_id))
            # print("Mensaje email: {}".format(email_message))
            # print("Testimonio: {}".format(student_testimony))

            result_message = "Reporte generado y enviado con éxito"
            
        except Exception as e:
            print(f"Error: {e}")

            result_message = "Error en la generación y envío de reporte"
        
        return render(request, 'send_report_to_donor.html', {
            "result_message" : result_message
        })


    return render(request, 'send_report_to_donor.html')


"""
Receives certain information, obtains the basic format of the report, and fills in 
the available fields with the information received.
"""
def generate_general_report(date, semester, student, testimony, non_academic_activities, crea_assistance):
    report_name = "Reporte general {} - {}.docx".format(student.student_code, semester)
    output_path = f'archivos/reportes/{report_name}'
    output_path_pdf = f'archivos/reportes/{report_name.replace(".docx", ".pdf")}'

    
    # Reads the format content
    format_content = read_report_format()

    # Creates a new doc to add the modifications
    modified_doc = Document()

    for paragraph_info in format_content:
        new_paragraph = modified_doc.add_paragraph()

        # Replaces the fields with the information received as parameters
        paragraph_text = paragraph_info['paragraph_text']
        paragraph_text = paragraph_text.replace("[Fecha]", semester)
        paragraph_text = paragraph_text.replace("[estudiante]", str(student.name))
        paragraph_text = paragraph_text.replace("[semestre]", semester)
        paragraph_text = paragraph_text.replace("[testimonio_estudiante]", testimony)
        paragraph_text = paragraph_text.replace("[actividades_no_académicas]", str(non_academic_activities))
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
    convert(output_path, output_path_pdf)


"""
Reads a .docx document containing the basic format of the report to be generated. 
"""
def read_report_format():
    doc = Document('./crud/static/formats/Reporte general beneficiario.docx')

    doc_content = []

    accumulated_paragraph = ''

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