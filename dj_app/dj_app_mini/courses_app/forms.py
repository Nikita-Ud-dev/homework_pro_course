from django import forms
from .models import Course
# from homework_pro_course.dj_app.dj_app_mini.members_app.models import User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'direction', 'description', 'list_of_members', 'limit_members']
        widgets = {
            'list_of_members': forms.CheckboxSelectMultiple,
        }

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super().__init__(*args, **kwargs)
    #     if user:
    #         self.fields['']
