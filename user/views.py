from django.shortcuts import render
from .models import User
from django.views import View
from django.http import JsonResponse
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class CreateUserView(View):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)
        
class UserListView(APIView):
    def get(self, response):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# import jwt
# from django.conf import settings
# from datetime import datetime

        # payload = {
        #     'user_id': user.id,
        #     'exp' : datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
        # }
        # token = jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)