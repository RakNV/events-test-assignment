from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Event, Registration
from datetime import datetime, timezone


class EventAPITests(APITestCase):
    def setUp(self):

        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.token1 = Token.objects.create(user=self.user1)
        self.user2 = User.objects.create_user(username='user2', password='password456')
        self.token2 = Token.objects.create(user=self.user2)

        self.event1 = Event.objects.create(
            title='Test Event 1',
            description='Test Description 1',
            date=datetime(2024, 12, 31, tzinfo=timezone.utc),
            location='Test Location 1',
            organizer=self.user1
        )
        self.event2 = Event.objects.create(
            title='Test Event 2',
            description='Test Description 2',
            date=datetime(2025, 1, 1, tzinfo=timezone.utc),
            location='Test Location 2',
            organizer=self.user2
        )

        self.client1 = APIClient()
        self.client1.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        self.client2 = APIClient()
        self.client2.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        self.unauth_client = APIClient()

    def _create_event_data(self):
        return {
            'title': 'New Event',
            'description': 'New Event Description',
            'date': '2024-12-31T00:00:00Z',
            'location': 'New Event Location'
        }

    # Test List Events
    def test_list_events_authenticated(self):
        url = reverse('event-list')
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_events_unauthenticated(self):
        url = reverse('event-list')
        response = self.unauth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test Get Single Event
    def test_get_valid_event(self):
        url = reverse('event-detail', args=[self.event1.id])
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.event1.title)

    def test_get_invalid_event(self):
        url = reverse('event-detail', args=[999])
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test Create Event
    def test_create_valid_event(self):
        url = reverse('event-create')
        data = self._create_event_data()
        response = self.client1.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 3)
        self.assertEqual(response.data['organizer'], self.user1.id)

    def test_create_event_invalid_data(self):
        url = reverse('event-create')
        data = self._create_event_data()
        data.pop('title')
        response = self.client1.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test Update Event
    def test_get_registered_events(self):
        Registration.objects.create(user=self.user1, event=self.event2)
        url = reverse('user-registered-events')
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.event2.id)

    def test_get_registered_events_empty(self):
        url = reverse('user-registered-events')
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_registered_events_unauthenticated(self):
        url = reverse('user-registered-events')
        response = self.unauth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_event_as_organizer(self):
        url = reverse('event-update', args=[self.event1.id])
        data = {
            'title': 'Updated Title',
            'description': self.event1.description,
            'date': self.event1.date.isoformat(),
            'location': self.event1.location
        }
        response = self.client1.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event1.refresh_from_db()
        self.assertEqual(self.event1.title, 'Updated Title')