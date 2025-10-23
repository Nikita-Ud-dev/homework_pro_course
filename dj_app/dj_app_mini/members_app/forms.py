from django import forms
from django.core.exceptions import ValidationError

from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'age', 'gender']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': "Введіть і'мя", 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': "Введіть фамілію", 'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'placeholder': "Введіть вік: від 16 до 40", 'class': 'form-control'}),
            # 'gender': forms.Select(attrs={'class': 'form-control'})
        }

        help_texts = {
            'first_name': "(Ввід: Обов'язково)",
            'last_name': "(Ввід: Не Обов'язково)",
            'age': "(Ввід: Обов'язково)",
            'gender': "(Вибір: Обов'язково)",
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 16:
            raise ValidationError('Учаснику не може бути менше 16 років')
        elif age > 40:
            raise ValidationError('Учаснику не може бути більше 40 років')
        return age

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['gender'].choices = self.fields['gender'].choices[1:]




