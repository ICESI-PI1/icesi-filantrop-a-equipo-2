from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import request
from .models import Student


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

def confirmacion(request):
    return render(request, 'students_confirm.html')


def guardar_estudiante(request):
    if request.method == "POST":
        idType = request.POST.get('tipo_documento')
        idNumber = request.POST.get('numero_documento')
        name = request.POST.get('nombre_completo')
        email = request.POST.get('correo_electronico')
        institutionalEmail = request.POST.get('correo_institucional')
        icfesScore = request.POST.get('puntaje_icfes')
        birthDate = request.POST.get('fecha_nacimiento')
        cellphoneNumber = request.POST.get('numero_celular')
        accumulatedAverage = request.POST.get('promedio_acumulado')
        creditsStudied = request.POST.get('creditos_cursados')
        genre = request.POST.get('genero')
        studentCode = request.POST.get('codigo_identificador')

        student = Student.objects.create(student_code=studentCode,
                                         name=name,
                                         genre=genre,
                                         id_type=idType,
                                         id_number=idNumber,
                                         email=email,
                                         institutional_email=institutionalEmail,
                                         icfes_score=icfesScore,
                                         birth_date=birthDate,
                                         cellphone_number=cellphoneNumber,
                                         accumulated_average=accumulatedAverage,
                                         credits_studied=creditsStudied)
        student.save()
        print(Student.objects.all())
        return render(request, 'students_info.html')
    return render(request, 'students_info.html')
