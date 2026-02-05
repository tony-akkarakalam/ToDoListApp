from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import TodoItem

class TodoFeatureTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')
        
        TodoItem.objects.create(user=self.user, title='High Task', priority='HIGH')
        TodoItem.objects.create(user=self.user, title='Low Task', priority='LOW')

    def test_filter_priority(self):
        response = self.client.get(reverse('todo-list'), {'priority': 'HIGH'})
        self.assertContains(response, 'High Task')
        self.assertNotContains(response, 'Low Task')

    def test_search(self):
        response = self.client.get(reverse('todo-list'), {'q': 'Low'})
        self.assertNotContains(response, 'High Task')
        self.assertContains(response, 'Low Task')
