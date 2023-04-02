from rest_framework import serializers
from .models import PersonalExpense

class PersonalExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalExpense
        fields = ('id', 'user', 'amount', 'memo', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

        def create(self, validated_data):
            user = self.context['user']
            validated_data['user'] = user
            return PersonalExpense.objects.create(**validated_data)

