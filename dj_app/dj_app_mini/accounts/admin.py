from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import CourseUser, ActionLog, BillingAdress
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Permission)

class CourseUserForm(forms.ModelForm):
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
        model = CourseUser
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput()
        }
@admin.register(CourseUser)
class CourseUserAdmin(UserAdmin):
    list_display = ('email', 'phone_number', 'is_active')
    ordering = ('-date_joined',)
    form = CourseUserForm

    fieldsets = (
        ('Особисті дані', {'fields': ('email', 'first_name', 'last_name', 'is_active', 'phone_number', 'date_of_birth')}),
        ('Зміна паролю', {'fields': ('new_password1', 'new_password2'), 'classes': ('collapse',)}),
        ('Права', {'fields': ('is_staff', 'is_superuser', 'user_permissions', 'groups'), 'classes': ('collapse',)}),

    )

@admin.register(ActionLog)
class ActionLogModel(admin.ModelAdmin):
    model = ActionLog
    list_display = ('name_log', 'model_log', 'user', 'action_type', 'timestamp', 'content_type', 'object_id')
