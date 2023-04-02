from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.models import User
from personalexpense.models import PersonalExpense
# Create your tests here.

class ExpenseCreateTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test,com', password='test_password')
        self.url = reverse('expense-create')
        self.client = APIClient()

    def test_create_expense(self):
        self.client.force_authenticate(user=self.user)

        data = {'amount': 1000, 'memo': '테스트 가계부 항목'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expense = PersonalExpense.objects.first()
        self.assertIsNotNone(expense)
        self.assertEqual(expense.user, self.user)
        self.assertEqual(expense.amount, 1000)
        self.assertEqual(expense.memo, '테스트 가계부 항목')

    def test_create_expense_without_login(self):
        data = {'amount': 1000, 'memo': '테스트 가계부 항목'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(PersonalExpense.objects.exists())