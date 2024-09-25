from django.test import TestCase

from rest_framework import status
from rest_framework import reverse
from rest_framework import APIClient

from .models import Post, Comment
from django.contrib.auth.models import User

class PostCommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_post(self):
        response = self.client.post(reverse('post_list'), {'title': ' Test Post', 'content': 'This is a test.'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment(self):
        post = Post.objects.create(title='Test Post', content='This is a test.', author=self.user)
        response = self.client.post(reverse('comment_list'),  {'post': post.id, 'content': 'Test Comment'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_update_post(self):
        response = self.client.put(reverse('post-detail', args=[self.post.id]), {'title': 'Updated Post', 'content': 'Updated content.'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')
        self.assertEqual(self.post.content, 'Updated content.')

    def test_delete_post(self):
        response = self.client.delete(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_update_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='Initial Comment')
        response = self.client.put(reverse('comment-detail', args=[comment.id]), {'content': 'Updated Comment'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated Comment')

    def test_delete_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='Initial Comment')
        response = self.client.delete(reverse('comment-detail', args=[comment.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_update_post_not_author(self):
        other_user = User.objects.create_user(username='otheruser', password='testpass')
        self.client.logout()
        self.client.login(username='otheruser', password='testpass')
        
        response = self.client.put(reverse('post-detail', args=[self.post.id]), {'title': 'Malicious Update', 'content': 'This should fail.'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_not_author(self):
        other_user = User.objects.create_user(username='otheruser', password='testpass')
        self.client.logout()
        self.client.login(username='otheruser', password='testpass')
        
        response = self.client.delete(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_comment_not_author(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='Initial Comment')
        other_user = User.objects.create_user(username='otheruser', password='testpass')
        self.client.logout()
        self.client.login(username='otheruser', password='testpass')
        
        response = self.client.put(reverse('comment-detail', args=[comment.id]), {'content': 'Malicious Update'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_not_author(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='Initial Comment')
        other_user = User.objects.create_user(username='otheruser', password='testpass')
        self.client.logout()
        self.client.login(username='otheruser', password='testpass')
        
        response = self.client.delete(reverse('comment-detail', args=[comment.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)