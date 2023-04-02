from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PersonalExpenseSerializer, ShortURLSerializer
from .models import PersonalExpense, ShortURL
from django.utils import timezone
from datetime import timedelta


class ExpenseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PersonalExpenseSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenseUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return PersonalExpense.objects.get(pk=pk, user=user)
        except PersonalExpense.DoesNotExist:
            return None

    def put(self, request, pk):
        expense = self.get_object(pk, request.user)
        if expense is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PersonalExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense = self.get_object(pk, request.user)
        if expense is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExpenseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = PersonalExpense.objects.filter(user=request.user)
        serializer = PersonalExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExpenseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return PersonalExpense.objects.get(pk=pk, user=user)
        except PersonalExpense.DoesNotExist:
            return None

    def get(self, request, pk):
        expense = self.get_object(pk, request.user)
        if expense is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PersonalExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExpenseCloneView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return PersonalExpense.objects.get(pk=pk, user=user)
        except PersonalExpense.DoesNotExist:
            return None

    def post(self, request, pk):
        original_expense = self.get_object(pk, request.user)
        if original_expense is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 복제된 가계부 항목 생성
        cloned_expense = PersonalExpense.objects.create(
            user=request.user,
            amount=original_expense.amount,
            memo=original_expense.memo
        )
        serializer = PersonalExpenseSerializer(cloned_expense)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExpenseShortURLView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return PersonalExpense.objects.get(pk=pk, user=user)
        except PersonalExpense.DoesNotExist:
            return None

    def post(self, request, pk):
        expense = self.get_object(pk, request.user)
        if expense is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        expires_at = timezone.now() + timedelta(days=1)
        short_url = ShortURL.objects.create(expense=expense, expires_at=expires_at)
        short_url.generate_short_url()
        short_url.save()

        serializer = ShortURLSerializer(short_url)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ExpenseShortURLDetailView(APIView):
    def get(self, request, short_url):
        try:
            short_url_instance = ShortURL.objects.get(short_url=short_url)
        except ShortURL.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if short_url_instance.expires_at < timezone.now():
            return Response(status=status.HTTP_410_GONE)

        expense = short_url_instance.expense
        serializer = PersonalExpenseSerializer(expense)
        return Response(serializer.data)
