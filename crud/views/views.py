from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from ..models import Office

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