from django.test import TestCase, Client
from django.urls import reverse
from crud.models import Beca, Archivo
from crud.views.forms import UploadFileForm
import pandas as pd
from io import BytesIO
from datetime import datetime


class LoadScholarshipDataTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Asegúrate de usar la URL correcta según tu configuración de URLs
        self.url = reverse('info-financiera')
        self.test_data_excel = None  # Variable para almacenar el archivo de prueba

    def tearDown(self):
        # Eliminar el archivo de prueba si existe
        if self.test_data_excel:
            self.test_data_excel.close()

    def test_get(self):
        # Crea un archivo de prueba
        test_data = pd.DataFrame({
            'id_estudiante': ['A00381234', 'A00385678'],
            'duracion': [1, 2],
            'tipo_beca': ['Beca1', 'Beca2'],
            'monto_asignado': [5000, 6000]
        })
        self.test_data_excel = BytesIO()
        test_data.to_excel(self.test_data_excel, index=False)
        self.test_data_excel.seek(0)
        self.test_data_excel.name = 'test_data.xlsx'

        # Guarda el archivo de prueba en la base de datos
        archivo = Archivo(
            nombre=self.test_data_excel.name,
            fecha=datetime.now(),
        )
        archivo.save()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scholarship_data.html')
        self.assertIsInstance(response.context['form'], UploadFileForm)
        archivos = response.context['archivos']
        self.assertEqual(len(archivos), 1)
        self.assertEqual(archivos[0].nombre, 'test_data.xlsx')

    def test_post_valid_form(self):
        # Crea un archivo de prueba
        test_data = pd.DataFrame({
            'id_estudiante': ['A00381234', 'A00385678'],
            'duracion': [1, 2],
            'tipo_beca': ['Beca1', 'Beca2'],
            'monto_asignado': [5000, 6000]
        })
        self.test_data_excel = BytesIO()
        test_data.to_excel(self.test_data_excel, index=False)
        self.test_data_excel.seek(0)
        self.test_data_excel.name = 'test_data.xlsx'

        response = self.client.post(
            self.url, {'file': self.test_data_excel}, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scholarship_data.html')

        becas = Beca.objects.all()
        self.assertEqual(len(becas), 2)
        self.assertEqual(becas[0].id_estudiante, 'A00381234')
        self.assertEqual(becas[1].id_estudiante, 'A00385678')
<<<<<<< HEAD
=======

    def test_post_invalid_form(self):
        # Prueba el manejo de un formulario inválido
        response = self.client.post(self.url, {}, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scholarship_data.html')
        self.assertFormError(response, 'form', 'file',
                             'This field is required')

    def test_post_invalid_file_format(self):
        # Prueba el manejo de un archivo con un formato no admitido
        invalid_file = BytesIO()
        invalid_file.name = 'invalid.txt'
        response = self.client.post(
            self.url, {'file': invalid_file}, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scholarship_data.html')
        self.assertFormError(response, 'form', 'file',
                             'File format not supported')

    def test_post_file_with_empty_data(self):
        # Prueba el manejo de un archivo con datos vacíos
        empty_data = pd.DataFrame()
        empty_data_excel = BytesIO()
        empty_data.to_excel(empty_data_excel, index=False)
        empty_data_excel.seek(0)
        empty_data_excel.name = 'empty_data.xlsx'
        response = self.client.post(
            self.url, {'file': empty_data_excel}, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scholarship_data.html')
        self.assertContains(response, 'No data found in the file')

    def test_post_invalid_data(self):
        # Prueba el manejo de un archivo con datos inválidos
        invalid_data = pd.DataFrame({
            'id_estudiante': ['A00381234', 'A00385678'],
            'duracion': [1, 2],
            'tipo_beca': ['Beca1', 'Beca2'],
        })
        invalid_data_excel = BytesIO()
        invalid_data.to_excel(invalid_data_excel, index=False)
        invalid_data_excel.seek(0)
        invalid_data_excel.name = 'invalid_data.xlsx'
        response = self.client.post(
            self.url, {'file': invalid_data_excel}, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scholarship_data.html')
        self.assertContains(response, 'Missing columns in the file')

    def test_post_exception_handling(self):
        # Prueba el manejo de excepciones al procesar el archivo
        invalid_file = BytesIO()
        invalid_file.name = 'invalid_file.xlsx'
        response = self.client.post(
            self.url, {'file': invalid_file}, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scholarship_data.html')
        self.assertContains(
            response, 'An error occurred while processing the file')

    def test_get_archivos_empty(self):
        # Prueba el caso en el que no hay archivos en la base de datos
        Archivo.objects.all().delete()  # Borra todos los archivos
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scholarship_data.html')
        self.assertNotContains(response, 'Historial de Archivos Subidos')
>>>>>>> 09a774910f560d45a94368c72b2f2dcbfe5925f3
