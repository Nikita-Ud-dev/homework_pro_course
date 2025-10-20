from wsgiref.validate import validator

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import ForeignKey, ManyToManyField


# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=30)
    direction = models.CharField(max_length=70, default="None", null=False)
    description = models.TextField(max_length=500,  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    list_of_members = ManyToManyField('members_app.Member', blank=True, related_name='courses')
    limit_members = models.PositiveIntegerField(default=5, null=False, validators=[MinValueValidator(5), MaxValueValidator(100)])


    def __str__(self):
        return self.title