from django.urls import path
from courses_app.views import (
    course_list, create_course, update_course, delete_course, history_course_logs,
    teacher_list, create_teacher, update_teacher, delete_teacher, history_teacher_logs,

    CourseListView, AdminCourseListView, UserCourseListView, CourseCreateView, CourseUpdateView,
    CourseDeleteView, CourseHistoryLogsView,

    TeacherListView, AdminTeacherListView, UserTeacherListView, TeacherCreateView, TeacherUpdateView,
    TeacherDeleteView, TeacherHistoryLogsView,
)

app_name = 'courses_app'

urlpatterns = [
    path('', course_list, name='course_list'),
    path('list/', course_list, name='course_list'),
    path('create_course/', create_course, name='create_course'),
    path('update_course/<int:course_id>/', update_course, name='update_course'),
    path('history_course_logs/<int:course_id>/', history_course_logs, name='history_course_logs'),
    path('delete_course/<int:course_id>/', delete_course, name='delete_course'),

    path('list_cbv/', CourseListView.as_view(), name='courses_list_cbv' ),
    path('create_cbv/', CourseCreateView.as_view(), name='create_course_cbv' ),
    path('update_cbv/<int:course_id>/', CourseUpdateView.as_view(), name='update_course_cbv' ),
    path('delete_cbv/<int:course_id>/', CourseDeleteView.as_view(), name='delete_course_cbv' ),
    path('logs_cbv/<int:course_id>/', CourseHistoryLogsView.as_view(), name='history_logs_course_cbv' ),
    path('admin_list_cbv/', AdminCourseListView.as_view(), name='admin_list_cbv' ),
    path('user_list_cbv/', UserCourseListView.as_view(), name='user_list_cbv' ),

    path('teacher_list_cbv/', TeacherListView.as_view(), name='teachers_list_cbv'),
    path('create_teacher_cbv/', TeacherCreateView.as_view(), name='create_teacher_cbv'),
    path('update_teacher_cbv/<int:teacher_id>/', TeacherUpdateView.as_view(), name='update_teacher_cbv'),
    path('delete_teacher_cbv/<int:teacher_id>/', TeacherDeleteView.as_view(), name='delete_teacher_cbv'),
    path('teacher_logs_cbv/<int:teacher_id>/', TeacherHistoryLogsView.as_view(), name='history_logs_teacher_cbv'),

    path('teacher_list/', teacher_list, name='teacher_list'),
    path('create_teacher/', create_teacher, name='create_teacher'),
    path('update_teacher/<int:teacher_id>/', update_teacher, name='update_teacher'),
    path('delete_teacher/<int:teacher_id>/', delete_teacher, name='delete_teacher'),
    path('history_teacher_logs/<int:teacher_id>/', history_teacher_logs, name='history_teacher_logs'),
]