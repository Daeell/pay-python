from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from user.models import User
from personalexpense.models import PersonalExpense, ShortURL
from django.utils import timezone
from datetime import timedelta

class ExpenseShortURLTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client = APIClient()
        self.expense = PersonalExpense.objects.create(user=self.user, amount=1000, memo='가계부 항목 1')
        self.url = reverse('expense-short-url', kwargs={'pk': self.expense.pk})

    def test_create_short_url_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        short_url = ShortURL.objects.get(expense=self.expense)
        self.assertIsNotNone(short_url)
        self.assertIsNotNone(response.data['short_url'])
        self.assertIsNotNone(response.data['expires_at'])

    def test_create_short_url_unauthenticated(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_short_url_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('expense-short-url', kwargs={'pk': self.expense.pk + 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ExpenseShortURLDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.expense = PersonalExpense.objects.create(user=self.user, amount=1000, memo='가계부 항목 1')
        expires_at = timezone.now() + timedelta(days=1)
        self.short_url = ShortURL.objects.create(expense=self.expense,expires_at=expires_at)
        self.short_url.generate_short_url()
        self.short_url.save()
        self.url = reverse('expense-detail-short-url', kwargs={'short_url': self.short_url.short_url})

    def test_view_short_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.expense.pk)
        self.assertEqual(int(float(response.data['amount'])), self.expense.amount)
        self.assertEqual(response.data['memo'], self.expense.memo)

    def test_view_expired_short_url(self):
        self.short_url.expires_at = timezone.now() - timedelta(minutes=1)
        self.short_url.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_410_GONE)
