from django.urls import path , include
from members_app.views import member_list, create_member, update_member, delete_member, history_member_logs

app_name = 'members_app'

urlpatterns = [
    path('', member_list, name='member_list'),
    path('list/', member_list, name='member_list'),
    path('create_member/', create_member, name='create_member'),
    path('update_member/<int:member_id>', update_member, name='update_member'),
    path('history_member_logs/<int:member_id>', history_member_logs, name='history_member_logs'),
    path('delete_member/<int:member_id>', delete_member, name='delete_member'),
]