from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from user_profile.models import User


class UserAccountTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('user-register')
        self.login_url = reverse('user-login')
        self.profile_url = reverse('user-profile-update')
        self.password_reset_url = reverse('password-reset')

        self.user_data = {
            "email": "user@example.com",
            "username": "testuser",
            "password": "password123",
            "password_confirm": "password123"
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="user@example.com").exists())

    def test_login_user(self):
        # Avval ro'yxatdan o'tkazamiz
        self.client.post(self.register_url, self.user_data)
        user = User.objects.get(email="user@example.com")
        user.is_verified = True
        user.save()

        login_data = {
            "email": "user@example.com",
            "password": "password123"
        }

        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.token = response.data["access"]

    def test_get_user_profile(self):
        self.client.post(self.register_url, self.user_data)
        user = User.objects.get(email="user@example.com")
        user.is_verified = True
        user.save()

        login_data = {
            "email": "user@example.com",
            "password": "password123"
        }

        login_response = self.client.post(self.login_url, login_data)
        token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['email'], "user@example.com")

    def test_password_reset(self):
        self.client.post(self.register_url, self.user_data)
        user = User.objects.get(email="user@example.com")
        response = self.client.post(self.password_reset_url, {"email": user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertIsNotNone(user.email_token)
