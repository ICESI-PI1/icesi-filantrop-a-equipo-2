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