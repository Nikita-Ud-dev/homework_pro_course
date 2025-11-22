from django.urls import path , include
from members_app.views import (
    member_list, create_member, update_member, delete_member, history_member_logs,

    MemberListView, AdminMemberListView, UserMemberListView, MemberCreateView, MemberUpdateView,
    MemberDeleteView, MemberHistoryLogsView,
)

app_name = 'members_app'

urlpatterns = [
    path('', member_list, name='member_list'),
    path('list/', member_list, name='member_list'),
    path('create_member/', create_member, name='create_member'),
    path('update_member/<int:member_id>', update_member, name='update_member'),
    path('history_member_logs/<int:member_id>', history_member_logs, name='history_member_logs'),
    path('delete_member/<int:member_id>', delete_member, name='delete_member'),

    path('members_list_cbv/', MemberListView.as_view(), name='members_list_cbv' ),
    path('member_create_cbv/', MemberCreateView.as_view(), name='member_create_cbv' ),
    path('member_update_cbv/<int:member_id>/', MemberUpdateView.as_view(), name='member_update_cbv' ),
    path('member_delete_cbv/<int:member_id>/', MemberDeleteView.as_view(), name='member_delete_cbv' ),
    path('logs_cbv/<int:member_id>/', MemberHistoryLogsView.as_view(), name='history_logs_member_cbv' ),
    path('admin_list_cbv/', AdminMemberListView.as_view(), name='admin_list_cbv' ),
    path('user_list_cbv/', UserMemberListView.as_view(), name='user_list_cbv' ),
]