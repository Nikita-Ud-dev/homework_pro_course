from django.urls import path , include
from .views import member_list, create_member, update_member, delete_member

app_name = 'members_app'

urlpatterns = [
    path('', member_list, name='member_list'),
    path('list/', member_list, name='member_list'),
    path('create_member/', create_member, name='create_member'),
    path('update_member/<int:member_id>', update_member, name='update_member'),
    path('delete_member/<int:member_id>', delete_member, name='delete_member'),
]