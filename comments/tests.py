from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post
from comments.models import Comment

User = get_user_model()

class CommentAPITestCase(APITestCase):
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

    def assertCommentState(self, comment, expected_likes_count, liked_users):
        self.assertEqual(comment.likes.count(), expected_likes_count)
        self.assertEqual(comment.likes_count, expected_likes_count)
        for user in liked_users:
            self.assertIn(user, comment.likes.all())
        for user in set(User.objects.all()) - set(liked_users):
            self.assertNotIn(user, comment.likes.all())

    def test_comment_creation(self):
        comment = self.comment
        self.assertEqual(comment.content, 'This is a test comment')
        self.assertEqual(comment.author, self.user2)
        self.assertEqual(comment.post, self.post)
        self.assertTrue(comment.is_active)
        self.assertCommentState(comment, 0, [])

    def test_like_comment(self):
        self.comment.likes.add(self.user1)
        self.comment.likes_count = self.comment.likes.count()
        self.comment.save()
        self.assertCommentState(self.comment, 1, [self.user1])

    def test_unlike_comment(self):
        self.comment.likes.add(self.user1)
        self.comment.likes.remove(self.user1)
        self.comment.likes_count = self.comment.likes.count()
        self.comment.save()
        self.assertCommentState(self.comment, 0, [])
