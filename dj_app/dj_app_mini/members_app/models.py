from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from members_app.gender_models import GenderChoices
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Member(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='members')
    # course = models.ForeignKey('courses_app.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    age = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(16), MaxValueValidator(40)])
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, blank=False, null=False)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.first_name

