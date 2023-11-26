from django.shortcuts import render
from crud.models import Beca, Student
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

@login_required
def listar_alumnos(request):
    alumnos = Student.objects.all()
    for alumno in alumnos:
        try:
            beca = Beca.objects.get(id_estudiante=alumno.student_code)
            alumno.beca = beca
        except Beca.DoesNotExist:
            alumno.beca = None
    return render(request, "ListaAlumnos.html", {"alumnos": alumnos})