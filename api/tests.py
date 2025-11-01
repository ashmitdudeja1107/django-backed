from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task, Note

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_signup(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }
        response = self.client.post('/api/auth/signup/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
    
    def test_login(self):
        User.objects.create_user(username='testuser', password='testpass123')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class TaskTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
    
    def test_create_task(self):
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'pending'
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'Test Task')
    
    def test_list_tasks(self):
        Task.objects.create(user=self.user, title='Task 1')
        Task.objects.create(user=self.user, title='Task 2')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_mark_task_complete(self):
        task = Task.objects.create(user=self.user, title='Task 1')
        response = self.client.post(f'/api/tasks/{task.id}/mark_complete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertTrue(task.completed)

class NoteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(user=self.user, title='Test Task')
    
    def test_create_note(self):
        data = {
            'title': 'Test Note',
            'content': 'Test Content',
            'task': self.task.id
        }
        response = self.client.post('/api/notes/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
    
    def test_list_notes_by_task(self):
        Note.objects.create(user=self.user, task=self.task, title='Note 1', content='Content 1')
        Note.objects.create(user=self.user, task=self.task, title='Note 2', content='Content 2')
        response = self.client.get(f'/api/notes/?task={self.task.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)