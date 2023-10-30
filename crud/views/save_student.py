from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from crud.models import Student
from datetime import datetime
import pandas as pd
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

        # Comprueba si la fecha de nacimiento es válida
        try:
            birth_date = datetime.strptime(data['fecha_nacimiento'], '%d/%m/%Y')
            if birth_date > datetime.now():
                return False, "La fecha de nacimiento no puede ser en el futuro."
        except ValueError:
            return False, "Formato de fecha de nacimiento inválido. Debe ser DD/MM/AAAA."

        # Comprueba si el número de celular es válido
        if not re.fullmatch(r'\d{10}', data['numero_celular']):
            return False, "El número de celular debe tener 10 dígitos."

        # Comprueba si el puntaje ICFES está en el rango válido
        if not 0 <= int(data['puntaje_icfes']) <= 500:
            return False, "El puntaje ICFES debe estar entre 0 y 500."

        # Comprueba si el promedio acumulado y los créditos cursados son números válidos
        if not 0 <= float(data['promedio_acumulado']) <= 5.0:
            return False, "El promedio acumulado debe estar entre 0 y 5."
        if not 0 <= int(data['creditos_cursados']):
            return False, "Los créditos cursados no pueden ser negativos."

        # Comprueba si el género es válido
        if data['genero'] not in ['Masculino', 'Femenino', 'Otro']:
            return False, "El género debe ser 'Masculino', 'Femenino' o 'Otro'."

        return True, ""
    except Exception as e:
        # Agrega un manejo de excepciones para posibles errores aquí.
        return False, "Error en la validación de datos: " + str(e)


def guardar_estudiante(request):
    message = ''
    if request.method == "POST":
        try:
            received_file = request.FILES['file_students']
            file = pd.read_excel(received_file)
            for index, row in file.iterrows():
                fields = {
                    'id_type': row['tipo_documento'],
                    'id_number': row['numero_documento'],
                    'name': row['nombre_completo'],
                    'email': row['correo_electronico'],
                    'institutional_email': row['correo_institucional'],
                    'icfes_score': row['puntaje_icfes'],
                    'birth_date': row['fecha_nacimiento'],
                    'cellphone_number': row['numero_celular'],
                    'accumulated_average': row['promedio_acumulado'],
                    'credits_studied': row['creditos_cursados'],
                    'genre': row['genero'],
                    'student_code': row['codigo_identificador']
                }
                exists_row = Student.objects.filter(student_code=row['codigo_identificador'],
                                                    name=row['nombre_completo'],
                                                    genre=row['genero'],
                                                    id_type=row['tipo_documento'],
                                                    id_number=row['numero_documento'],
                                                    email=row['correo_electronico'],
                                                    institutional_email=row['correo_institucional'],
                                                    icfes_score=row['puntaje_icfes'],
                                                    birth_date=row['fecha_nacimiento'],
                                                    cellphone_number=row['numero_celular'],
                                                    accumulated_average=row['promedio_acumulado'],
                                                    credits_studied=row['creditos_cursados'])
                if exists_row.exists():
                    exists_row.update(**fields)
                else:
                    student = Student.objects.create(**fields)
                    student.save()
        except Exception as e:
            message = str(e)

        data = {
            'id_type': request.POST.get('tipo_documento'),
            'id_number': request.POST.get('numero_documento'),
            'name': request.POST.get('nombre_completo'),
            'email': request.POST.get('correo_electronico'),
            'institutional_email': request.POST.get('correo_institucional'),
            'icfes_score': request.POST.get('puntaje_icfes'),
            'birth_date': request.POST.get('fecha_nacimiento'),
            'cellphone_number': request.POST.get('numero_celular'),
            'accumulated_average': request.POST.get('promedio_acumulado'),
            'credits_studied': request.POST.get('creditos_cursados'),
            'genre': request.POST.get('genero'),
            'student_code': request.POST.get('codigo_identificador')
        }
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
    return render(request, 'students_info.html', {'result_message': message})
