from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from crud.models import Office, Student 

import smtplib
from email.mime.text import MIMEText

def home(request):
    return render(request, 'home.html')

"""
Renders the view to make a request, to an office, to update a student's information.

When the user fills all the fields, this method receives the information and calls the send email function.
"""
@login_required
def ask_info_update(request):
    if request.method == 'POST':
        selected_office_id = request.POST.get('offices')

        try:
            selected_office = Office.objects.get(id=selected_office_id)
        except Office.DoesNotExist:
            return HttpResponse('La oficina seleccionada no existe')

        send_email(selected_office.email)

        return redirect(home)

    offices = Office.objects.all()
    students = Student.objects.all()

    return render(request, 'ask_update_info.html', {
        'offices' : offices,
        'students' : students
    })


"""
Given a destinatary, sends an email, form the default mail.
"""
def send_email(receiver_email):
    subject = "Solicitud de actualización de información"
    message = "Por favor, actualice la información, amiguito bello."

    sender = "pi.seg.estudiantes@gmail.com"
    password = "zhazuuahhicywuyg"

    mail = MIMEText(message)
    mail['From'] = sender
    mail['To'] = receiver_email
    mail['Subject'] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as gmail_server:
        gmail_server.starttls()
        gmail_server.login(sender, password)

        gmail_server.send_message(mail)