from django.urls import path
from .views import course_list, create_course, update_course, delete_course

app_name = 'courses_app'

urlpatterns = [
    path('', course_list, name='course_list'),
    path('list/', course_list, name='course_list'),
    path('create_course/', create_course, name='create_course'),
    path('update_course/<int:course_id>/', update_course, name='update_course'),
    path('delete_course/<int:course_id>/', delete_course, name='delete_course'),
]