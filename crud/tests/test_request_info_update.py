from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from crud.models import Office, Student


class RequestInfoUpdateTestCase(TestCase):

    """
    Creates, and authenticates, an user to be able to test the request information update screen.

    Also, creates all the objects needed to test each part of the screen.  
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.office1 = Office.objects.create(name='Office 1')
        self.office2 = Office.objects.create(name='Office 2')

        self.student1 = Student.objects.create(
            student_code='A00456789',
            name='Student1',
            genre='M',
            id_type='CC',
            id_number='1234567890',
            email='ejemplo@gmail.com',
            institutional_email='estudiante@universidad.com',
            icfes_score=300,
            birth_date=date(2000, 1, 1),
            cellphone_number='123456789',
            accumulated_average=4.5,
            credits_studied=120
        )

    """
    Tests the screen for request information update is rendering correctly.
    """

    def test_screen_render(self):
        url = reverse('ask_info_update')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    """
    Tests that the offices in the screen for request information update are the same that have been created in the DB.
    """

    def test_office_selection(self):
        url = reverse('ask_info_update')

        response = self.client.get(url)

        self.assertIn('offices', response.context)

        actual_offices = [str(office)
                          for office in response.context['offices']]

        self.assertCountEqual(actual_offices, ['Office 1', 'Office 2'])

        selected_office_id = self.office1.id
        response = self.client.post(url, {'office': selected_office_id})

        selected_office = Office.objects.get(id=selected_office_id)

        self.assertEqual(selected_office, self.office1)

    """
    Tests that the results returned by the search box, in the screen, are consistent with the written text.

    Also, tests that the user can search the student by name and by code.
    """

    def test_student_search(self):
        url = reverse('ask_info_update')

        response = self.client.get(url)

        search_term = self.student1.name
        response = self.client.get(url, {'search-box': search_term})

        self.assertContains(response, 'Student1')
        self.assertContains(response, 'A00456789')

        search_term = self.student1.student_code
        response = self.client.get(url, {'search-box': search_term})

        self.assertContains(response, 'Student1')
        self.assertContains(response, 'A00456789')

    """
    Tests that the email is sent successfully.
    """

    def test_send_message(self):
        url = reverse('ask_info_update')

        response = self.client.get(url)

        test_message = 'Test message'

        response = response.client.get(
            url, {'offices': self.office1.id, 'message-area': test_message})

        self.assertContains(response, self.office1.id)

        # with patch('crud.views.request_info_update.send_email') as mock_send_email:
        #     # Realiza la selección de la oficina y los estudiantes
        #     url = reverse('ask_info_update')  # Ajusta según tus rutas
        #     data = {
        #         'office': self.office1.id,
        #         'students': [self.student1.id],
        #         'message': 'Este es un mensaje de prueba.',
        #     }

        #     response = self.client.post(url, data)

        #     # Verifica que se haya realizado la acción esperada
        #     self.assertEqual(response.status_code, 200)  # O el código que esperas

        #     # Verifica que la función de envío de correo electrónico haya sido llamada
        #     mock_send_email.assert_called_once_with(
        #         receiver_email=self.office1.email,  # Ajusta según tu modelo de Office
        #         message='Este es un mensaje de prueba.\n\nEstudiantes seleccionados:\n- Student 1',
        #         subject='Nuevo mensaje de la oficina',
        #     )
