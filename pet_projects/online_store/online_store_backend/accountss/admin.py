from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.transaction import commit
from django.core.exceptions import ValidationError

from accountss.models import OnlineStoreUser, Roles
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Register your models here.

# admin.site.register(OnlineStoreUser)
admin.site.register(Roles)

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateOnlineStoreUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Введіть пароль',
        widget=forms.PasswordInput,
        required=True,
        help_text='Введіть пароль сюди'
    )
    password2 = forms.CharField(
        label='Підтвердження паролю',
        widget=forms.PasswordInput,
        required=True,
    )


    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 == password2:
            raise ValidationError('Паролі не співпадають')
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = OnlineStoreUser
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'roles', 'date_of_birth', 'profile_picture']
        widgets = {
            'date_of_birth': DateInput()
        }

class OnlineStoreUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Поточний Пароль', help_text='Зашифрована версія паролю')

    new_password1 = forms.CharField(
        label='Новий пароль',
        widget=forms.PasswordInput,
        required=False,
        help_text='Залиште пустим якщо не хочете змінювати пароль'
    )
    new_password2 = forms.CharField(
        label='Підтвердження паролю',
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = OnlineStoreUser
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput()
        }

@admin.register(OnlineStoreUser)
class OnlineStoreUserAdmin(UserAdmin):
    list_display = ('email', 'phone_number', 'is_active')
    ordering = ('-date_joined',)
    form = OnlineStoreUserForm
    add_form = CreateOnlineStoreUserForm
    filter_horizontal = ('roles',)

    add_fieldsets = (
        ('Особисті дані', {'fields': ('email', 'phone_number', 'first_name', 'last_name', 'date_of_birth', 'profile_picture',)}),
        ('Пароль', {'fields': ('password1', 'password2'), 'classes': ('collapse',)}),
        ('Права', {'fields': ('roles',), 'classes': ('collapse',)}),
    )
    fieldsets = (
        ('Особисті дані', {'fields': ('email', 'password', 'first_name', 'last_name', 'is_active', 'phone_number', 'date_of_birth', 'rating_count')}),
        ('Зміна паролю', {'fields': ('new_password1', 'new_password2'), 'classes': ('collapse',)}),
        ('Права', {'fields': ('is_staff', 'is_superuser', 'user_permissions', 'groups', 'roles'), 'classes': ('collapse',)}),
    )