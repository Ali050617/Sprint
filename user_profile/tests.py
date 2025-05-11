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



# FOLLOW TEST

class UserFollowAPITest(APITestCase):
    def setUp(self):
        self.user1_data = {
            "email": "user1@example.com",
            "username": "user1",
            "password": "testpass123",
            "password_confirm": "testpass123"
        }

        self.user2_data = {
            "email": "user2@example.com",
            "username": "user2",
            "password": "testpass123",
            "password_confirm": "testpass123"
        }

        self.client.post(reverse('user-register'), self.user1_data)
        self.client.post(reverse('user-register'), self.user2_data)

        self.user1 = User.objects.get(email=self.user1_data['email'])
        self.user2 = User.objects.get(email=self.user2_data['email'])

        self.user1.is_verified = True
        self.user2.is_verified = True
        self.user1.save()
        self.user2.save()

        response = self.client.post(reverse('user-login'), {
            "email": self.user1_data["email"],
            "password": self.user1_data["password"]
        })
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_email_verification(self):
        self.user1.is_verified = False
        self.user1.generate_email_token()
        self.user1.save()

        url = reverse("verify-email")
        response = self.client.post(url, {"token": self.user1.email_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertTrue(self.user1.is_verified)

    def test_follow_user(self):
        url = reverse("user-follow", kwargs={"username": self.user2.username})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user2.user_profile in self.user1.user_profile.following.all())

    def test_unfollow_user(self):
        follow_url = reverse("user-follow", kwargs={"username": self.user2.username})
        self.client.post(follow_url)

        unfollow_url = reverse("user-unfollow", kwargs={"username": self.user2.username})
        response = self.client.post(unfollow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user2.user_profile in self.user1.user_profile.following.all())

    def test_followers_list(self):
        self.client.post(reverse("user-follow", kwargs={"username": self.user2.username}))
        url = reverse("user-followers", kwargs={"username": self.user2.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['user']['username'], self.user1.username)

    def test_following_list(self):
        self.client.post(reverse("user-follow", kwargs={"username": self.user2.username}))
        url = reverse("user-following", kwargs={"username": self.user1.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['user']['username'], self.user2.username)

