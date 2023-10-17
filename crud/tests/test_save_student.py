from django.test import TestCase, RequestFactory
from django.urls import reverse
from crud.models import Student
from crud.views.save_student import guardar_estudiante, validar_datos


class TestGuardarEstudiante(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_creacion_estudiante(self):
        data = {
            'tipo_documento': 'CC',
            'numero_documento': '123456789',
            'nombre_completo': 'Juan Perez',
            'correo_electronico': 'juan.perez@example.com',
            'correo_institucional': 'jperez@university.edu',
            'puntaje_icfes': '350',
            'fecha_nacimiento': '2000-01-01',
            'numero_celular': '3001234567',
            'promedio_acumulado': '4.5',
            'creditos_cursados': '120',
            'genero': 'M',
            'codigo_identificador': '001'
        }
        request = self.factory.post(reverse('guardar_estudiante'), data)
        response = guardar_estudiante(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Student.objects.filter(student_code=data['codigo_identificador']).exists())


    def test_guardar_estudiante_get(self):
        request = self.factory.get(reverse('guardar_estudiante'))
        response = guardar_estudiante(request)
        self.assertEqual(response.status_code, 200)

    def test_creacion_estudiante_sin_datos(self):
        # Prueba la creación de un estudiante sin proporcionar datos
        request = self.factory.post(reverse('guardar_estudiante'))
        response = guardar_estudiante(request)
        self.assertEqual(response.status_code, 400)  # Debe devolver un código de estado 400 (BadRequest)

    def test_validar_datos(self):
        # Prueba con todos los campos requeridos
        data = {
            'tipo_documento': 'CC',
            'numero_documento': '123456789',
            'nombre_completo': 'Juan Perez',
            'correo_electronico': 'juan.perez@example.com',
            'correo_institucional': 'juan.perez@institution.com',
            'puntaje_icfes': '350',
            'fecha_nacimiento': '2000-01-01',
            'numero_celular': '3001234567',
            'promedio_acumulado': '4.5',
            'creditos_cursados': '120',
            'genero': 'M',
            'codigo_identificador': '001'
        }
        is_valid, message = validar_datos(data)
        self.assertTrue(is_valid)

        # Prueba con algunos campos requeridos vacíos
        data['nombre_completo'] = ''
        is_valid, message = validar_datos(data)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Todos los campos son requeridos.")

        # Prueba con correos electrónicos no válidos
        data['nombre_completo'] = 'Juan Perez'
        data['correo_electronico'] = 'invalid_email'
        is_valid, message = validar_datos(data)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Por favor, introduce un correo electrónico válido.")

    def test_guardar_estudiante_correo_institucional_invalido(self):
        data = {
            'tipo_documento': 'CC',
            'numero_documento': '123456789',
            'nombre_completo': 'Juan Perez',
            'correo_electronico': 'juan.perez@example.com',
            'correo_institucional': 'correo_institucional_invalido',  # Correo inválido
            'puntaje_icfes': '350',
            'fecha_nacimiento': '2000-01-01',
            'numero_celular': '3001234567',
            'promedio_acumulado': '4.5',
            'creditos_cursados': '120',
            'genero': 'M',
            'codigo_identificador': '003'
        }
        request = self.factory.post(reverse('guardar_estudiante'), data)
        response = guardar_estudiante(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Por favor, introduce un correo electrónico válido.", response.content.decode())
        self.assertFalse(Student.objects.filter(student_code=data['codigo_identificador']).exists())

