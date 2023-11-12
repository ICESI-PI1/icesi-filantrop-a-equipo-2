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
            semester = str(f'{date.year} - {1}') if date.month <=6 else str(f'{date.year} - {2}')

            generate_general_report(date, semester, selected_student, student_testimony)

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


def generate_general_report(date, semester, student, testimony):
    report_name = "Reporte general {} - {}.docx".format(student.student_code, semester)
    output_path = f'archivos/reportes/{report_name}'
    
    # Reads the format content
    format_content = read_report_format()

    # Crear un nuevo documento de Word modificado
    modified_doc = Document()

    for paragraph_info in format_content:
        new_paragraph = modified_doc.add_paragraph()

        # new_paragraph.text = new_paragraph.text.replace("[Fecha]", str(date))
        # new_paragraph.text = new_paragraph.text.replace("[estudiante]", str(student.name))
        # new_paragraph.text = new_paragraph.text.replace("[semestre]", semester)
        # new_paragraph.text = new_paragraph.text.replace("[testimonio]", testimony)

        for run_info in paragraph_info['runs']:
            new_run = new_paragraph.add_run(run_info['text'])

            # new_run = new_paragraph.add_run(run_info['font_italic'])
            new_run.font.size = Pt(run_info['font_size']) if run_info['font_size'] else None
            new_run.font.bold = run_info['font_bold']
            new_run.font.italic = run_info['font_italic']
            new_run.font.name = run_info['font_name']
            new_paragraph.alignment = run_info['alignment']

        print(new_paragraph.text)

    # Guardar el documento de Word modificado como PDF
    modified_doc.save(output_path)


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