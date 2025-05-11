from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post
from comments.models import Comment


class CommentModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='pass123')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='pass123')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user1
        )
        self.comment = Comment.objects.create(
            content='This is a test comment',
            author=self.user2,
            post=self.post
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'This is a test comment')
        self.assertEqual(self.comment.author, self.user2)
        self.assertEqual(self.comment.post, self.post)
        self.assertTrue(self.comment.is_active)
        self.assertEqual(self.comment.likes_count, 0)
        self.assertEqual(self.comment.likes.count(), 0)

    def test_like_comment(self):
        self.comment.likes.add(self.user1)
        self.comment.likes_count = self.comment.likes.count()
        self.comment.save()

        self.assertEqual(self.comment.likes.count(), 1)
        self.assertEqual(self.comment.likes_count, 1)
        self.assertIn(self.user1, self.comment.likes.all())

    def test_unlike_comment(self):
        self.comment.likes.add(self.user1)
        self.comment.likes.remove(self.user1)
        self.comment.likes_count = self.comment.likes.count()
        self.comment.save()

        self.assertEqual(self.comment.likes.count(), 0)
        self.assertEqual(self.comment.likes_count, 0)
        self.assertNotIn(self.user1, self.comment.likes.all())
