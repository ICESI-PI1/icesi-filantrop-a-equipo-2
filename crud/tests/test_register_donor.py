from django.test import TestCase, Client
from django.urls import reverse
from crud.models import Donor


class DonorRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.save_donor_url = reverse('save_donor')

    def test_save_donor(self):
        data = {
            'nombre': 'Test',
            'apellido': 'Donor',
            'tipo_persona': 'PN',
            'numero_nit': '123456',
            'correo_electronico': 'test@example.com',
            'descripcion': 'Test Donor',
            'colaboraciones_previas': 'None'
        }

        response = self.client.post(self.save_donor_url, data)

        self.assertEqual(response.status_code, 200)

        donor = Donor.objects.get(nit='123456')
        self.assertIsNotNone(donor)

        self.assertEqual(donor.name, 'Test')
        self.assertEqual(donor.lastname, 'Donor')
        self.assertEqual(donor.nit, '123456')
        self.assertEqual(donor.email, 'test@example.com')
        self.assertEqual(donor.description, 'Test Donor')
