from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class SigninViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_signin_GET(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_signin_POST_valid_credentials(self):
        response = self.client.post(
            reverse('signin'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_signin_POST_invalid_credentials(self):
        response = self.client.post(
            reverse('signin'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, "Usuario o contraseña es incorrecto.")
