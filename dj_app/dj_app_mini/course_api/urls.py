from django.urls import path, include
from rest_framework.routers import DefaultRouter
from course_api.views import (
    CourseViewSet, ActionLogViewSet, TeacherViewSet, MemberViewSet,
    CourseTokenObtainPair, CourseTokenRefreshPair

)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'action-log', ActionLogViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'members', MemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('course-token/', CourseTokenObtainPair.as_view(), name='course_token_obtain_pair'),
    path('course-token/refresh/', CourseTokenRefreshPair.as_view(), name='course_token_refresh'),
]