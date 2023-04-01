from django.shortcuts import render
import json

from .models import User
from django.views import View
from django.http import JsonResponse


# Create your views here.
class ResgisterView(View):
    def post(self, request):
        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'error' : '이메일과 비밀번호를 입력해주세요'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error' : '이미 등록된 이메일입니다.'}, status=400)

        User.objects.create_user(
            email = email,
            password = password
        )
        return JsonResponse({'message' : '회원가입 성공'}, status=201)

    def get(self, response):
        User_data = User.objects.values()
        return JsonResponse({'유저정보' : list(User_data)}, status=200)

# import jwt
# from django.conf import settings
# from datetime import datetime

        # payload = {
        #     'user_id': user.id,
        #     'exp' : datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
        # }
        # token = jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)