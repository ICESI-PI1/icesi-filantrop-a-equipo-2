from django.http import HttpResponseBadRequest
from django.shortcuts import render
from crud.models import Student
from django.db import IntegrityError, transaction
import re


def validar_datos(data):
    try:
        for key, value in data.items():
            if not value:
                return False, "Todos los campos son requeridos."

        # Comprueba si los correos electrónicos son válidos
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(email_regex, data['correo_electronico']) or not re.fullmatch(email_regex,
                                                                                         data['correo_institucional']):
            return False, "Por favor, introduce un correo electrónico válido."

        return True, ""
    except Exception as e:
        # Agrega un manejo de excepciones para posibles errores aquí.
        return False, "Error en la validación de datos: " + str(e)


def guardar_estudiante(request):
    message = ''
    if request.method == "POST":
        data = {
            'tipo_documento': request.POST.get('tipo_documento'),
            'numero_documento': request.POST.get('numero_documento'),
            'nombre_completo': request.POST.get('nombre_completo'),
            'correo_electronico': request.POST.get('correo_electronico'),
            'correo_institucional': request.POST.get('correo_institucional'),
            'puntaje_icfes': request.POST.get('puntaje_icfes'),
            'fecha_nacimiento': request.POST.get('fecha_nacimiento'),
            'numero_celular': request.POST.get('numero_celular'),
            'promedio_acumulado': request.POST.get('promedio_acumulado'),
            'creditos_cursados': request.POST.get('creditos_cursados'),
            'genero': request.POST.get('genero'),
            'codigo_identificador': request.POST.get('codigo_identificador')
        }

        # Verificar si los datos requeridos están presentes
        if not all(data.values()):
            return HttpResponseBadRequest("Todos los campos son requeridos.")

        is_valid, message = validar_datos(data)
        if not is_valid:
            return render(request, 'students_info.html', {'message': message})

        try:
            with transaction.atomic():
                student = Student.objects.create(student_code=data['codigo_identificador'],
                                                 name=data['nombre_completo'],
                                                 genre=data['genero'],
                                                 id_type=data['tipo_documento'],
                                                 id_number=data['numero_documento'],
                                                 email=data['correo_electronico'],
                                                 institutional_email=data['correo_institucional'],
                                                 icfes_score=data['puntaje_icfes'],
                                                 birth_date=data['fecha_nacimiento'],
                                                 cellphone_number=data['numero_celular'],
                                                 accumulated_average=data['promedio_acumulado'],
                                                 credits_studied=data['creditos_cursados'])
                student.save()
                message = 'Estudiante guardado con éxito.'
        except IntegrityError:
            message = 'No se pudo guardar el estudiante debido a un error de integridad de datos.'
        except Exception as e:
            message = str(e)

    return render(request, 'students_info.html', {'message': message})
