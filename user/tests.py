from django.test import TestCase
from django.urls import reverse
from user.models import User

class CreateUserViewTest(TestCase):
    def test_create_user_success(self):
        url = reverse('create_user')
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }

        response = self.client.post(url, data, content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_create_user_fail_duplicate_email(self):
        User.objects.create_user(email='test@example.com', password='password123')

        url = reverse('create_user')
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }

        response = self.client.post(url, data, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('email')[0], 'user with this 이메일 already exists.')

# 추가된 테스트 케이스
class UserListViewTest(TestCase):
    def test_get_user_list_success(self):
        User.objects.create_user(email='test1@example.com', password='password123')
        User.objects.create_user(email='test2@example.com', password='password123')

        url = reverse('user_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
