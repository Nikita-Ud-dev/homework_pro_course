from django import forms
from courses_app.models import Course, Teacher


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'direction', 'teacher', 'description', 'list_of_members', 'limit_members']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введіть назву курсу', 'class': 'form-control'}),
            'direction': forms.TextInput(attrs={'placeholder': 'Введіть назву напрямку', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Введіть опис', 'class': 'form-control'}),
            'list_of_members': forms.CheckboxSelectMultiple,
            'limit_members': forms.NumberInput(attrs={'placeholder': 'Введіть ліміт учасників: від 5 до 100', 'class': 'form-control'}),
        }

        help_texts = {
            'title': "(Ввід: Обов'язково)",
            'direction': "(Ввід: Обов'язково)",
            'description': "(Ввід: Не обов'язково)",
            # 'list_of_members': f'(Додавання учасників: Не повинно перевищувати "Ліміт учасників":)',
            'limit_members': "(Ввід: Обов'язково)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            limit = instance.limit_members
            self.fields['list_of_members'].help_text = (
                f'(Додавання учасників: Не повинно перевищувати "Ліміт учасників": {limit})'
            )
        # else:
        #     self.fields['list_of_members'].help_text = (
        #         'Додавання учасників: Не повинно перевищувати ліміт (значення буде визначено пізніше)'
        #     )


    def clean(self):
        cleaned_data = super().clean()
        members = self.cleaned_data.get('list_of_members')
        limit = self.cleaned_data.get('limit_members')

        if members and limit and len(members) > limit:
            self.add_error('list_of_members', f'Кількість учасників не може перевищувати {limit}.')
        return cleaned_data

    # def clean_list_of_members(self):
    #     members = self.cleaned_data.get('list_of_members')
    #     limit = self.cleaned_data.get('limit_members')
    #     if members and limit and members > limit:
    #         raise forms.ValidationError(f'Кількість учасників не може перевищувати {limit}.')
    #     return members

    def clean_teacher(self):
        teacher = self.cleaned_data.get('teacher')
        if not teacher:
            raise forms.ValidationError('Виберіть "викладача"')
        return teacher

    def clean_limit_members(self):
        limit = self.cleaned_data.get('limit_members')
        if limit < 5:
            raise forms.ValidationError('Ліміт не може бути нижче 5')
        elif limit > 100:
            raise forms.ValidationError('Ліміт не може бути більше 100')
        return limit

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super().__init__(*args, **kwargs)
    #     if user:
    #         self.fields['']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'age', 'gender']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': "Введіть і'мя", 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': "Введіть фамілію", 'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'placeholder': "Введіть вік: від 22 до 55", 'class': 'form-control'}),
        }

        help_texts = {
            'first_name': "(Ввід: Обов'язково)",
            'last_name': "(Ввід: Не Обов'язково)",
            'course': "(Вибір: Обов'язково)",
            'age': "(Ввід: Обов'язково)",
            'gender': "(Вибір: Обов'язково)",
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 22:
            raise forms.ValidationError('Учаснику не може бути менше 22 років')
        elif age > 55:
            raise forms.ValidationError('Учаснику не може бути більше 55 років')
        return age

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['gender'].choices = self.fields['gender'].choices[1:]

