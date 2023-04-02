from django.db import models
from user.models import User
import uuid

class PersonalExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount} - {self.memo}"

    class Meta:
        db_table = 'personal_expense'

class ShortURL(models.Model):
    expense = models.OneToOneField(PersonalExpense, on_delete=models.CASCADE)
    short_url = models.CharField(max_length=6, unique=True, editable=False)
    expires_at = models.DateTimeField()

    def generate_short_url(self):
        short_url = uuid.uuid4().hex[:6]
        while ShortURL.objects.filter(short_url=short_url).exists():
            short_url = uuid.uuid4().hex[:6]
        self.short_url = short_url
    
    class Meta:
        db_table = 'short_url'