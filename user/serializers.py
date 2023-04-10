from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'created_at', 'updated_at', 'is_active', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError('이 계정은 비활성화되었습니다.')
            else:
                raise serializers.ValidationError('이메일 또는 비밀번호가 잘못되었습니다.')
        else:
            raise serializers.ValidationError('이메일과 비밀번호를 입력해주세요.')

        data['user'] = user
        return data
        