from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class PostModelAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user
        )

    def test_get_post_list(self):
        response = self.client.get('/api/posts/')  # замените на актуальный URL
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Post',
            'content': 'Some content here',
            'author': self.user.id
        }
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, 201)

