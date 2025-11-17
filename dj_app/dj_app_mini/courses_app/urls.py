from django.urls import path
from courses_app.views import (
    course_list, create_course, update_course, delete_course, history_course_logs,
    teacher_list, create_teacher, update_teacher, delete_teacher, history_teacher_logs
)

app_name = 'courses_app'

urlpatterns = [
    path('', course_list, name='course_list'),
    path('list/', course_list, name='course_list'),
    path('create_course/', create_course, name='create_course'),
    path('update_course/<int:course_id>/', update_course, name='update_course'),
    path('history_course_logs/<int:course_id>/', history_course_logs, name='history_course_logs'),
    path('history_teacher_logs/<int:teacher_id>/', history_teacher_logs, name='history_teacher_logs'),
    path('delete_course/<int:course_id>/', delete_course, name='delete_course'),
    path('teacher_list/', teacher_list, name='teacher_list'),
    path('create_teacher/', create_teacher, name='create_teacher'),
    path('update_teacher/<int:teacher_id>/', update_teacher, name='update_teacher'),
    path('delete_teacher/<int:teacher_id>/', delete_teacher, name='delete_teacher'),
]