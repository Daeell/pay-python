from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.models import User
from personalexpense.models import PersonalExpense

class ExpenseListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client = APIClient()
        self.url = reverse('expense-list')

        for i in range(5):
            PersonalExpense.objects.create(user=self.user, amount=1000 * (i + 1), memo=f'가계부 항목 {i + 1}')

    def test_expense_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        for i, expense in enumerate(response.data):
            self.assertEqual(expense['amount'], f'{1000 * (i + 1)}.00')
            self.assertEqual(expense['memo'], f'가계부 항목 {i + 1}')

    def test_expense_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)