from django.urls import path
from accounts.views import action_logs_list

app_name = 'accounts'

urlpatterns = [
    path('list/', action_logs_list, name='action_logs_list')
]