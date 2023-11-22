from django.shortcuts import render, redirect
from crud.models import Alerta, Student
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def crear_alerta(request):
    result_message = None

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        student_code = request.POST.get('student_code')
        descripcion = request.POST.get('descripcion')

        try:
            alumno = Student.objects.get(student_code=student_code)
            Alerta.objects.create(
                tipo=tipo,
                student_code=student_code,
                name=alumno.name,
                descripcion=descripcion,
            )
            result_message = 'Alerta creada exitosamente.'
        except Student.DoesNotExist:
            result_message = 'Error: Estudiante no encontrado.'
        except Exception as e:
            result_message = f'Error al crear la alerta: {str(e)}'

    alumnos = Student.objects.all()
    return render(request, 'send_notifications.html', {'alumnos': alumnos, 'result_message': result_message})
