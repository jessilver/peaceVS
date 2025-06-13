from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.test import TestCase
from .models import UserProfile

User = get_user_model()

class AuthTokenTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            is_active=True
        )
        self.token_url = reverse('api_token_auth')

    def test_token_auth_success(self):
        response = self.client.post(self.token_url, {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_token_auth_wrong_password(self):
        response = self.client.post(self.token_url, {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_token_auth_nonexistent_user(self):
        response = self.client.post(self.token_url, {
            'email': 'notfound@example.com',
            'password': 'irrelevant'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='user1@example.com',
            password='testpass',
            first_name='User',
            last_name='One'
        )
        self.assertEqual(user.email, 'user1@example.com')
        self.assertTrue(user.check_password('testpass'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass',
            first_name='Admin',
            last_name='User'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, 'admin@example.com')

    def test_email_is_unique(self):
        User.objects.create_user(email='unique@example.com', password='pass', first_name='A', last_name='B')
        with self.assertRaises(Exception):
            User.objects.create_user(email='unique@example.com', password='pass', first_name='C', last_name='D')

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='profile@example.com', password='pass', first_name='Profile', last_name='User')

    def test_create_user_profile(self):
        profile = UserProfile.objects.create(
            user=self.user,
            nome_perfil='Perfil 1',
            avatar_url='http://example.com/avatar.png',
            data_nascimento='2000-01-01',
            preferencias_linguagem='pt-BR',
            eh_perfil_infantil=True
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.nome_perfil, 'Perfil 1')
        self.assertTrue(profile.eh_perfil_infantil)
        self.assertEqual(profile.preferencias_linguagem, 'pt-BR')
