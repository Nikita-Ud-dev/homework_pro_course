from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from accountss.models import Roles

User = get_user_model()

@receiver(user_logged_in)
def last_user_login(sender, user, request, **kwargs):
    user.last_date_login = timezone.now()
    user.save(update_fields=['last_date_login'])

@receiver(post_save, sender=User)
def set_role_admin(sender, instance, created, **kwargs):
    if instance.is_superuser and created:
        role = Roles.objects.get(name_role='admin')
        instance.roles.add(role)


