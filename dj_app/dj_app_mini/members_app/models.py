from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .gender_models import GenderChoices

# Create your models here.

class Member(models.Model):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=30, default='Unknown', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # course = models.ForeignKey('courses_app.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    age = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(16), MaxValueValidator(40)])
    gender = models.CharField(choices=GenderChoices.choices, default='None', blank=False)

    def __str__(self):
        return self.first_name

