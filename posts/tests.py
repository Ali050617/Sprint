from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post

class PostModelTest(TestCase):

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

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post content.')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertTrue(self.post.is_active)
        self.assertEqual(self.post.likes_count, 0)
        self.assertEqual(self.post.comments_count, 0)

    def test_str_method(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_update_fields(self):
        self.post.likes_count = 5
        self.post.comments_count = 3
        self.post.save()

        updated_post = Post.objects.get(id=self.post.id)
        self.assertEqual(updated_post.likes_count, 5)
        self.assertEqual(updated_post.comments_count, 3)
