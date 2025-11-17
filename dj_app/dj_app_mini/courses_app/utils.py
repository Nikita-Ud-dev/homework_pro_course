from dataclasses import field
from django.contrib.contenttypes.models import ContentType
from accounts.models import ActionLog
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from accounts.current_user import get_current_user
from courses_app.models import Course
from members_app.models import Member
def attach_generic(model_class, related_model, name=None, object_id_field='object_id', content_type_field='content_type'):
    if name is None:
        name = related_model.__name__.lower() + '_set'
    relation = GenericRelation(
        related_model,
        object_id_field=object_id_field,
        content_type_field=content_type_field,
        related_query_name=model_class.__name__.lower()
    )
    setattr(model_class, name, relation)
    print(f'added relation: {model_class.__name__}.{name}')
    return relation

for model in ActionLog.objects.get_queryset():
    related_model_class = model.content_type.model_class()
    if hasattr(related_model_class, 'actionlog_set'):
        continue
    else:
        attach_generic(related_model_class, ActionLog)

def get_logs(model_class):
    ctype = ContentType.objects.get_for_model(model_class)
    return ActionLog.objects.filter(content_type=ctype, object_id=model_class.id)