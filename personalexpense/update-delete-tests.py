from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.models import User
from personalexpense.models import PersonalExpense

class ExpenseUpdateDeleteTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com', password='test_password')
        self.expense = PersonalExpense.objects.create(user=self.user, amount=1000, memo='테스트 가계부 항목')
        self.url = reverse('expense-update-delete', kwargs={'pk': self.expense.pk})
        self.client = APIClient()

    # Expense update tests
    def test_update_expense(self):
        self.client.force_authenticate(user=self.user)

        data = {'amount': 2000, 'memo': '테스트 가계부 항목 업데이트'}
        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expense = PersonalExpense.objects.get(pk=self.expense.pk)
        self.assertEqual(expense.amount, 2000)
        self.assertEqual(expense.memo, '테스트 가계부 항목 업데이트')

    def test_partial_update_expense(self):
        self.client.force_authenticate(user=self.user)

        data = {'amount': 3000}
        response = self.client.put(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expense = PersonalExpense.objects.get(pk=self.expense.pk)
        self.assertEqual(expense.amount, 3000)
        self.assertEqual(expense.memo, '테스트 가계부 항목')

    def test_update_expense_unauthenticated(self):
        data = {'amount': 2000, 'memo': '테스트 가계부 항목 업데이트'}
        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_expense_not_found(self):
        self.client.force_authenticate(user=self.user)
        wrong_url = reverse('expense-update-delete', kwargs={'pk': self.expense.pk + 1})

        data = {'amount': 2000, 'memo': '테스트 가계부 항목 업데이트'}
        response = self.client.put(wrong_url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Expense delete tests
    def test_delete_expense(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PersonalExpense.objects.filter(pk=self.expense.pk).exists())

    def test_delete_expense_unauthenticated(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_expense_not_found(self):
        self.client.force_authenticate(user=self.user)
        wrong_url = reverse('expense-update-delete', kwargs={'pk': self.expense.pk + 1})

        response = self.client.delete(wrong_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)