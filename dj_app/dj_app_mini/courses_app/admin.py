from django.contrib import admin
from .models import Course
from .forms import CourseForm
# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('list_of_members',)