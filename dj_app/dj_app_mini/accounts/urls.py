from django.urls import path
from accounts.views import (
    action_logs_list,
    LogListView,
)

app_name = 'accounts'

urlpatterns = [
    path('list/', action_logs_list, name='action_logs_list'),
    path('list_cbv/', LogListView.as_view(), name='action_logs_list_cbv'),
]