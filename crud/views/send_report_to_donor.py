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


def home(request):
    return render(request, 'home.html')


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

            generate_general_report(date, selected_student, student_testimony)

            # print("Donante: {}".format(selected_donor))
            # print("Estudiante: {}".format(selected_student_id))
            # print("Mensaje email: {}".format(email_message))
            # print("Testimonio: {}".format(student_testimony))

            result_message = "Reporte generado y enviado con éxito"
            
        except Exception as e:
            print(e)
            result_message = "Error en la generación y envío de reporte"
        
        return render(request, 'send_report_to_donor.html', {
            "result_message" : result_message
        })


    return render(request, 'send_report_to_donor.html')


def generate_general_report(date, student, testimony):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, "Reporte PDF")

    # Cierra el lienzo y devuelve la respuesta
    p.showPage()
    p.save()

    relative_path = "archivos/reportes generales/"  # Ruta relativa al directorio de tu aplicación
    full_path = os.path.join(settings.BASE_DIR, relative_path)

    # Asegúrate de que la carpeta exista, si no, créala
    os.makedirs(full_path, exist_ok=True)

    print(full_path)

    # Guardar el archivo PDF en la carpeta
    with open(os.path.join(full_path, "reporte.pdf"), "wb") as pdf_file:
        pdf_file.write(response.content)

    return response

# def generate_general_report(date, student, testimony, non_academic_report, crea_report, academic_report):


#     return response