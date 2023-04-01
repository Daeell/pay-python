from django.test import TestCase
from django.urls import reverse
from user.models import User
# Create your tests here.

class RegisterViewTest(TestCase):
    def test_register_success(self):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }

        response = self.client.post(url, data, content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_register_fail_duplicate_email(self):
        User.objects.create_user(email='test@example.com', password='password123')

        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }

        response = self.client.post(url,data, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), '이미 등록된 이메일입니다.')