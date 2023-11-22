from django.shortcuts import render
from crud.models import Student, Donor
from django.http import HttpRequest

def listar_dnts(request):
    donantes = Donor.objects.all()
    for donante in donantes:
        # Obtenemos los estudiantes asociados a este donante
        estudiantes_asociados = Student.objects.filter(donor=donante.id)
        
        # Convertimos el QuerySet a una lista
        donante.estudiantes_asociados = list(estudiantes_asociados)
    return render(request, "ListaDonantes.html", {"donantes": donantes})

