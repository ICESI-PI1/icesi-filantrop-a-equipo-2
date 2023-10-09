from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from crud.models import Student


# Create your views here.

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
        return render(request, 'students_info.html')
    return render(request, 'students_info.html')
