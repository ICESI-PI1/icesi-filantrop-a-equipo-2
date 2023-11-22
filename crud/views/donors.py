from django.db import IntegrityError, transaction
from django.shortcuts import render
from crud.models import Donor
import re
from django.contrib.auth.decorators import login_required


@login_required
def validate_data(data):
    try:
        for key, value in data.items():
            if not value:
                return False, "Todos los campos son requeridos."

        # Comprueba si los correos electrónicos son válidos
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(email_regex, data['email']) or not re.fullmatch(email_regex,
                                                                            data['correo_institucional']):
            return False, "Por favor, introduce un correo electrónico válido."

        # Comprueba si el tipo_persona es válido
        if data['tipo_persona'] not in ['Persona natural', 'Persona jurídica']:
            return False, "El tipo de persona debe ser 'Natural' o 'Jurídica'."

        return True, ""
    except Exception as e:
        # Agrega un manejo de excepciones para posibles errores aquí.
        return False, "Error en la validación de datos: " + str(e)


def save_donor(request):
    if request.method == 'POST':
        try:
            data = {
                'name': request.POST.get('nombre'),
                'lastname': request.POST.get('apellido'),
                'type': request.POST.get('tipo_persona'),
                'nit': request.POST.get('numero_nit'),
                'email': request.POST.get('correo_electronico'),
                'description': request.POST.get('descripcion'),
                'previous_colaborations': request.POST.get('colaboraciones_previas')
            }

            if all(data.values()):
                is_valid, message = validate_data(data)

            try:
                with transaction.atomic():
                    donor, created = Donor.objects.update_or_create(
                        nit=request.POST.get('numero_nit'),
                        defaults=data
                    )
                    if created:
                        message = "Donante creado con éxito."
                    else:
                        message = "Donante actualizado con éxito."

            except Exception as e:
                print(e)
                message = "Error al crear el donante: " + str(e)

            return render(request, 'create_donor.html', {'message': message})

        except Exception as e:
            message = "Error al crear el donante: " + str(e)

    return render(request, 'create_donor.html')
