from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from courses_app.models import Course, Teacher
from courses_app.forms import CourseForm, TeacherForm
from courses_app.utils import get_logs
from accounts.current_user import set_current_user
# Create your views here.

@login_required
def course_list(request):
    courses = Course.objects.annotate(count_members=Count('list_of_members'))
    return render(request, 'course/course_list.html', {'courses': courses})

@login_required
def create_course(request):
    if request.method == 'POST':
        set_current_user(request.user)
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            return redirect('courses_app:course_list')
    else:
        form = CourseForm()
    return render(request,'course/create_course.html', {'form': form})

@login_required
def update_course(request, course_id):
    course = get_object_or_404(Course,id=course_id)
    if request.method == 'POST':
        set_current_user(request.user)
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            # members = form.cleaned_data['list_of_members']
            # limit = form.cleaned_data['limit_members']
            # if len(members) > limit:
            #     form.add_error('list_of_members', f'Кількість учасників не може перевищувати {limit}.')
            form.save()
            return redirect('courses_app:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request,'course/update_course.html', {'form': form})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('courses_app:course_list')
    else:
        return render(request, 'course/course_confirm_delete.html', {'course':course})

def history_course_logs(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    logs = get_logs(course)
    count_logs = logs.count()
    return render(request, 'course/history_logs.html', {
        'logs': logs,
        'count_logs': count_logs,
    })

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher/teacher_list.html', {'teachers': teachers})

@login_required
def create_teacher(request):
    if request.method == 'POST':
        set_current_user(request.user)
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.save()
            return redirect('courses_app:teacher_list')
    else:
        form = TeacherForm()
    return render(request,'teacher/create_teacher.html', {'form': form})

@login_required
def update_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher,id=teacher_id)
    if request.method == 'POST':
        set_current_user(request.user)
        form =TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('courses_app:teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request,'teacher/update_teacher.html', {'form': form})

@login_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        set_current_user(request.user)
        teacher.delete()
        return redirect('courses_app:teacher_list')
    else:
        return render(request, 'teacher/teacher_confirm_delete.html', {'teacher':teacher})

def history_teacher_logs(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    logs = get_logs(teacher)
    count_logs = logs.count()
    return render(request, 'teacher/history_logs.html', {
        'logs': logs,
        'count_logs': count_logs,
    })