from django.contrib import admin
from accounts.models import CourseUser, ActionLog, BillingAdress

# Register your models here.

admin.site.register(CourseUser)

@admin.register(ActionLog)
class ActionLogModel(admin.ModelAdmin):
    model = ActionLog
    list_display = ('name_log', 'model_log', 'user', 'action_type', 'timestamp', 'content_type', 'object_id')
