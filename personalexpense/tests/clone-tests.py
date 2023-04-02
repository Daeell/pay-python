from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.models import User
from personalexpense.models import PersonalExpense

class ExpenseCloneTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client = APIClient()
        self.expense = PersonalExpense.objects.create(user=self.user, amount=1000, memo='가계부 항목 1')
        self.url = reverse('expense-clone', kwargs={'pk': self.expense.pk})

    def test_expense_clone_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data['id'], self.expense.pk)
        self.assertEqual(response.data['amount'], '1000.00')
        self.assertEqual(response.data['memo'], '가계부 항목 1')

    def test_expense_clone_unauthenticated(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

   
