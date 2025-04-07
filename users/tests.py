from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }
        self.existing_user = User.objects.create_user(
            username='existinguser',
            password='existingpass',
            email='existing@example.com'
        )

    # Signup Tests
    def test_valid_signup(self):
        url = reverse('register')
        response = self.client.post(url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

        user = User.objects.get(username=self.valid_payload['username'])
        self.assertEqual(user.email, self.valid_payload['email'])

        self.assertTrue(user.check_password(self.valid_payload['password']))

        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_signup_duplicate_username(self):
        url = reverse('register')
        payload = {
            'username': 'existinguser',
            'password': 'newpass123',
            'email': 'new@example.com'
        }
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_signup_missing_required_fields(self):
        url = reverse('register')
        invalid_payloads = [
            {'password': 'pass123', 'email': 'test@example.com'},
            {'username': 'testuser', 'email': 'test@example.com'},
        ]

        for payload in invalid_payloads:
            response = self.client.post(url, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Login Tests
    def test_valid_login(self):
        url = reverse('login')
        credentials = {
            'username': 'existinguser',
            'password': 'existingpass'
        }
        response = self.client.post(url, credentials)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        token = Token.objects.get(user=self.existing_user)
        self.assertEqual(response.data['token'], token.key)

    def test_login_invalid_password(self):
        url = reverse('login')
        credentials = {
            'username': 'existinguser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, credentials)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    def test_login_missing_credentials(self):
        url = reverse('login')
        invalid_payloads = [
            {'password': 'existingpass'},
            {'username': 'existinguser'},
            {},
        ]

        for payload in invalid_payloads:
            response = self.client.post(url, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['detail'], 'Username and password required')

    def test_login_nonexistent_user(self):
        url = reverse('login')
        credentials = {
            'username': 'nonexistent',
            'password': 'password123'
        }
        response = self.client.post(url, credentials)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid credentials')