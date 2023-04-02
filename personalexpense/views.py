from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PersonalExpenseSerializer

class ExpenseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PersonalExpenseSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ExpenseUpdateDeleteView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk, user):
#         try:
#             return PersonalExpense.objects.get(pk=pk, user=user)
#         except PersonalExpense.DoesNotExist:
#             return None

# class ExpenseUpdateDeleteView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):
#         try:
#             return PersonalExpense.objects.get(pk=pk, user=self.request.user)
#         except PersonalExpense.DoesNotExist:
#             return None
        
#     def put(self, request, pk):
#         expense = self.get_object(pk)
#         if expense is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = PersonalExpenseSerializer(expense, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         expense = self.get_object(pk)
#         if expense is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         expense.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ExpenseListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         expenses = PersonalExpense.objects.filter(user=request.user)
#         serializer = PersonalExpenseSerializer(expenses, many=True)
#         return Response(serializer.data)