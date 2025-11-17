from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from accounts.models import ActionLog
from accounts.current_user import get_current_user
from django.contrib.contenttypes.models import ContentType
from members_app.models import Member

@receiver(post_save, sender=Member)
def member_log(sender, instance, created, **kwargs):
    user = get_current_user()
    if not user:
        return
    object_id = instance.pk
    if created:
        action_type = 'Створенно'
    else:
        action_type = 'Оновленно'
    ActionLog.objects.create(
        name_log=f'{sender.__name__}',
        user=user,
        action_type=action_type,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=object_id,
    )

@receiver(post_delete, sender=Member)
def member_log_delete(sender, instance, **kwargs):
    user = get_current_user()
    if not user:
        return
    object_id = instance.pk
    ActionLog.objects.create(
        name_log=f'{sender.__name__}',
        user=user,
        action_type='Видаленно',
        content_type=ContentType.objects.get_for_model(sender),
        object_id=object_id,
    )
