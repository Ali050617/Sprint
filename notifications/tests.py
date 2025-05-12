from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from user_profile.models import User
from posts.models import Post
from comments.models import Comment
from .models import Notification

class NotificationModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpassword'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post',
            author=self.user1
        )

    def test_notification_creation(self):
        notification = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='liked',
            target_type='post',
            target_id=self.post.id
        )

        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.actor, self.user2)
        self.assertEqual(notification.verb, 'liked')
        self.assertEqual(notification.target_type, 'post')
        self.assertEqual(notification.target_id, self.post.id)
        self.assertFalse(notification.is_read)

class NotificationAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpassword'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword'
        )

        self.client.force_authenticate(user=self.user1)

        self.notification1 = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='followed',
            target_type='profile',
            target_id=self.user1.id
        )

        self.notification2 = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='liked',
            target_type='post',
            target_id=1
        )

        self.notification3 = Notification.objects.create(
            recipient=self.user2,
            actor=self.user1,
            verb='commented',
            target_type='post',
            target_id=1
        )

    def test_get_user_notifications(self):
        url = reverse('notification-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        result = response.data['results'][0]
        self.assertEqual(result['recipient']['id'], self.user1.id)

    def test_filter_notifications_by_is_read(self):
        self.notification1.is_read = True
        self.notification1.save()

        url = reverse('notification-list') + '?is_read=false'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        url = reverse('notification-list') + '?is_read=true'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_mark_notification_as_read(self):
        url = reverse('mark-notification-read', args=[self.notification1.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_read'])

        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.is_read)

    def test_cannot_mark_others_notification_as_read(self):
        url = reverse('mark-notification-read', args=[self.notification3.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "You are not authorized to mark this notification as read")
        self.assertEqual(response.data['code'], "403")

    def test_mark_all_notifications_as_read(self):
        url = reverse('mark-all-notifications-read')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user1_notifications = Notification.objects.filter(recipient=self.user1)
        for notification in user1_notifications:
            self.assertTrue(notification.is_read)

        self.notification3.refresh_from_db()
        self.assertFalse(self.notification3.is_read)