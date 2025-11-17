from django.contrib import admin
from courses_app.models import Course, Teacher
from courses_app.forms import CourseForm

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('list_of_members',)

admin.site.register(Teacher)