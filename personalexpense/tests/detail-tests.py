from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.models import User
from personalexpense.models import PersonalExpense

class ExpenseDetailTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client = APIClient()
        self.expense = PersonalExpense.objects.create(user=self.user, amount=1000, memo='가계부 항목 1')
        self.url = reverse('expense-detail', kwargs={'pk': self.expense.pk})

    def test_expense_detail_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '1000.00')
        self.assertEqual(response.data['memo'], '가계부 항목 1')

    def test_expense_detail_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expense_detail_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('expense-detail', kwargs={'pk': self.expense.pk + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)