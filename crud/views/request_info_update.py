from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from crud.models import Office, Student

import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
import os

@login_required
def home(request):
    return render(request, 'home.html')


"""
Renders the view to make a request, to an office, to update a student's information.

When the user fills all the fields, this method receives the information and calls the send email function.
"""
@login_required
def ask_info_update(request):

    offices = Office.objects.all()
    students = Student.objects.all()

    if request.method == 'POST':
        try:
            selected_office_id = request.POST.get('offices')
            message = request.POST.get('message-area', '')

            selected_office = Office.objects.get(id=selected_office_id)

            subject = "Solicitud de actualización de información"

            send_email(selected_office.email, message, subject)

            result_message = "Actualización solicitada correctamente"

        except Exception:
            result_message = "Error al solicitar actualización"

            return render(request, 'ask_update_info.html', {
                'offices': offices,
                'students': students,
                'result_message': result_message
            })

        return render(request, 'ask_update_info.html', {
            'offices': offices,
            'students': students,
            'result_message': result_message
        })

    return render(request, 'ask_update_info.html', {
        'offices': offices,
        'students': students
    })


"""
Given a destinatary, a message, a subject, and an optional file, sends an email, from the default mail.
"""
@login_required
def send_email(receiver_email, message, subject, attachment_paths=None):
    sender = "pi.seg.estudiantes@gmail.com"
    password = "zhazuuahhicywuyg"

    mail = EmailMessage()
    mail.set_content(message)
    mail['From'] = sender
    mail['To'] = receiver_email
    mail['Subject'] = subject

    if attachment_paths:
        for attachment_path in attachment_paths:
            with open(attachment_path, 'rb') as file:
                content = file.read()
                filename = os.path.basename(attachment_path)

                # Changes MIME type depending on the file extension
                if filename.endswith('.pdf'):
                    mime_type = 'application/pdf'

                elif filename.endswith('.docx'):
                    mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

                else:
                    raise ValueError("Formato de archivo no admitido")
                
                mail.add_attachment(content, maintype='application', subtype=mime_type, filename=filename)
    
    with smtplib.SMTP("smtp.gmail.com", 587) as gmail_server:
        gmail_server.starttls()
        gmail_server.login(sender, password)

        gmail_server.send_message(mail)
