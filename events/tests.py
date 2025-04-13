
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Event

class EventTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            creator=self.user,
            is_virtual=True
        )
        
    def test_event_list_page(self):
        response = self.client.get(reverse('events:event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/list.html')
        
    def test_event_detail_page(self):
        response = self.client.get(reverse('events:event_detail', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/details.html')
        
    def test_create_event(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('events:event_create'), {
            'title': 'New Event',
            'description': 'New Description',
            'start_time': timezone.now(),
            'end_time': timezone.now() + timezone.timedelta(hours=2),
            'is_virtual': True
        })
        self.assertTrue(Event.objects.filter(title='New Event').exists())
        
    def test_my_events_page(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('events:my_events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/my_events.html')
