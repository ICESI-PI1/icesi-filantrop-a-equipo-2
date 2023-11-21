from django.test import TestCase, Client
from django.urls import reverse
from crud.models import Student, Document


class UploadFileTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Asegúrate de usar la URL correcta según tu configuración de URLs
        self.url = reverse('uploadFile')

    def test_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload_academic_report.html')
        self.assertIsNone(response.context.get('result_message'))
        self.assertQuerysetEqual(response.context['files'], [])

    def test_post_no_file(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload_academic_report.html')
        self.assertEqual(
            response.context['result_message'], 'No se proporcionó ningún archivo')
        self.assertQuerysetEqual(response.context['files'], [])

    def test_post_student_not_found(self):
        # Puedes modificar este test según tus necesidades
        # Asegúrate de que el código del estudiante aquí no exista en la base de datos
        response = self.client.post(self.url, {'uploadedFile': 'archivo.txt'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload_academic_report.html')
        self.assertIn('Estudiante no encontrado',
                      response.context['result_message'])
        self.assertQuerysetEqual(response.context['files'], [])

    def test_post_successful_upload(self):
        # Asegúrate de que el código del estudiante aquí exista en la base de datos
        student = Student.objects.create(
            student_code='codigo_estudiante_existente')

        # Simula un archivo cargado con un nombre específico
        with open('archivo.txt', 'rb') as file:
            response = self.client.post(self.url, {'uploadedFile': file})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload_academic_report.html')
        self.assertEqual(
            response.context['result_message'], 'Archivo cargado exitosamente')
        self.assertQuerysetEqual(response.context['files'], [repr(
            Document.objects.get(uploadedFile='archivo.txt'))])
