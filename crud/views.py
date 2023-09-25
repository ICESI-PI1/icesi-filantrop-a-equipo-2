from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import Office

import smtplib
from email.mime.text import MIMEText


# Create your views here.
def home(request):
    return render(request, 'home.html')


def signUp(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm,
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/postlog')
            except IntegrityError:
                return HttpResponse('Usuario ya existe')

            return HttpResponse('Contrasenas incorrectas')


def logIn(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return HttpResponse('No existe el usuario')
        else:
            login(request, user)
            return redirect("/postlog")


@login_required
def postLog(request):
    return render(request, 'logout.html')


@login_required
def singout(request):
    logout(request)
    return redirect(home)


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

    return render(request, 'ask_update_info.html', {
        'offices' : offices
    })


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

