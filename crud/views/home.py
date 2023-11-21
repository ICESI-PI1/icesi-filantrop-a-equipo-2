from django.shortcuts import render
from crud.models import Student, Donor
from django.http import HttpRequest

def listar_alumnos(request):
    alumnos=Student.objects.all()  
    return render(request, "ListaAlumnos.html",{"alumnos": alumnos})
 
def listar_donantes(request):
    donantes=Donor.objects.all()  
    return render(request, "ListaDonantes.html",{"donantes": donantes})

def contar_registers(request):
    donantes=Donor.objects.all()  
    cantidad_donantes = donantes.count()
    alumnos=Student.objects.all()  
    cantidad_alumnos = alumnos.count()
    return render (request, "home.html",{"cantidad_donantes": cantidad_donantes, "cantidad_alumnos": cantidad_alumnos})

