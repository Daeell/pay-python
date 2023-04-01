from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User

class CreateUserViewTest(TestCase):
    def test_create_user_success(self):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }

        response = self.client.post(url, data, content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_create_user_fail_duplicate_email(self):
        User.objects.create_user(email='test@example.com', password='password123')

        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }

        response = self.client.post(url, data, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('email')[0], 'user with this 이메일 already exists.')

class UserListViewTest(TestCase):
    def test_get_user_list_success(self):
        User.objects.create_user(email='test1@example.com', password='password123')
        User.objects.create_user(email='test2@example.com', password='password123')

        url = reverse('users')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

class LoginLogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password123')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_login_success(self):
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }

        response = self.client.post(self.login_url, data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())

    def test_login_fail_invalid_email(self):
        data = {
            'email': 'wrong@example.com',
            'password': 'password123'
        }

        response = self.client.post(self.login_url, data, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_login_fail_invalid_password(self):
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }

        response = self.client.post(self.login_url, data, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_logout_success(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        data = {
            'refresh': str(refresh)
        }

        response = self.client.post(self.logout_url, data, content_type='application/json', **headers)
        print(response.data)
        self.assertEqual(response.status_code, 205)

    def test_logout_fail_missing_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        data = {}

        response = self.client.post(self.logout_url, data, content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)

    def test_logout_fail_invalid_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        data = {
            'refresh': 'invalid_refresh_token'
        }

        response = self.client.post(self.logout_url, data, content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)