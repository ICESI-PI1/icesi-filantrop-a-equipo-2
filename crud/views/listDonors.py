from django.shortcuts import render, redirect
from crud.models import Student, Donor
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

@login_required
def listar_dnts(request):
    donantes = Donor.objects.all()
    for donante in donantes:
        # Obtenemos los estudiantes asociados a este donante
        estudiantes_asociados = Student.objects.filter(donor=donante.id)
        
        # Convertimos el QuerySet a una lista
        donante.estudiantes_asociados = list(estudiantes_asociados)

    if 'Filantropía' in request.user.user_type:
        return render(request, "ListaDonantes.html", {
            "donantes": donantes,
            "user": request.user
        })
    
    else:
        return redirect('/home/')

