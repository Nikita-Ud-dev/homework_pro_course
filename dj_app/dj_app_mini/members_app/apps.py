import sys
from django.apps import AppConfig

class MembersAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'members_app'

    def ready(self):
        if 'makemigrations' in sys.argv or 'migrate' in sys.argv:
            return
        else:
            from courses_app.utils import init_action_log_generic_relations
            init_action_log_generic_relations()