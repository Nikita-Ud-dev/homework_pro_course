from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import ForeignKey, ManyToManyField
from members_app.gender_models import GenderChoices
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=30)
    direction = models.CharField(max_length=70)
    description = models.TextField(max_length=500,  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='courses')
    teacher = models.OneToOneField('courses_app.Teacher', null=True, blank=True, on_delete=models.SET_NULL, related_name='course')
    list_of_members = ManyToManyField('members_app.Member', blank=True, related_name='courses')
    limit_members = models.PositiveIntegerField(null=False, validators=[MinValueValidator(5), MaxValueValidator(100)])


    def __str__(self):
        return self.title

class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='teachers')
    # course = models.OneToOneField('courses_app.Course', blank=False, null=True, on_delete=models.SET_NULL, related_name='teacher')
    age = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(22), MaxValueValidator(55)])
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, blank=False, null=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
