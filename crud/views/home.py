from django.shortcuts import render, redirect
from crud.models import Student, Donor, Alerta
from django.http import HttpRequest
from crud.views import listStudents

def listar_alertas(request):
    alertas= Alerta.objects.all()
    return render(request, "ListaAlertas.html",{"alertas": alertas})

def contar_registers(request):
    alertas= Alerta.objects.all()
    donantes=Donor.objects.all()  
    cantidad_donantes = donantes.count()
    alumnos=Student.objects.all()  
    cantidad_alumnos = alumnos.count()
    return render (request, "home.html",{"cantidad_donantes": cantidad_donantes, "cantidad_alumnos": cantidad_alumnos, "alertas": alertas})

def delete(request, id_alert):
    alerta = Alerta.objects.get(pk=id_alert)
    alerta.delete()
    alertas = Alerta.objects.all()
    donantes=Donor.objects.all()  
    cantidad_donantes = donantes.count()
    alumnos=Student.objects.all()  
    cantidad_alumnos = alumnos.count()
    return render(request, "home.html", {"alertas": alertas, "cantidad_donantes": cantidad_donantes, "cantidad_alumnos": cantidad_alumnos, "mensaje": 'OK'})

def delete_estudiantes(student_code):
    alumno = Student.objects.get(student_code=student_code)
    alumno.delete()
    alumnos = Student.objects.all()
    
    return redirect ('listar_alumnos')


def delete_donante(request, donor_id):
    donante = Donor.objects.get(id=donor_id)
    donante.delete()
    return redirect('listar_donantes')

