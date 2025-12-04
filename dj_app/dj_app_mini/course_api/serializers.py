from rest_framework import serializers
from courses_app.models import Course, Teacher
from members_app.models import Member
from accounts.models import ActionLog
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number']

class TeacherSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display', read_only=True)
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'age', 'gender',]

class CourseSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), source='teacher', write_only=True, required=False
    )
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'direction', 'description',
            'created_at', 'updated_at', 'creator', 'teacher',
            'teacher_id', 'list_of_members', 'limit_members',
        ]

class MemberSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display', read_only=True)
    class Meta:
        model = Member
        fields = [
            'id', 'first_name', 'last_name', 'age',
            'created_at', 'updated_at', 'gender',
        ]

class ActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionLog
        fields = '__all__'
