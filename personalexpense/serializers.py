from rest_framework import serializers
from .models import PersonalExpense, ShortURL

class PersonalExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalExpense
        fields = ('id', 'user', 'amount', 'memo', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

        def create(self, validated_data):
            user = self.context['user']
            validated_data['user'] = user
            return PersonalExpense.objects.create(**validated_data)

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['short_url', 'expires_at']