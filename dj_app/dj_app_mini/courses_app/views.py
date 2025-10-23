from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Course
from .forms import CourseForm
# Create your views here.

@login_required
def course_list(request):
    courses = Course.objects.annotate(count_members=Count('list_of_members'))
    return render(request, 'course/course_list.html', {'courses': courses})

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            # course.user = request.user
            course.save()
            return redirect('courses_app:course_list')
    else:
        form = CourseForm()
    return render(request,'course/create_course.html', {'form': form})

@login_required
def update_course(request, course_id):
    course = get_object_or_404(Course,id=course_id)
    if request.method == 'POST':
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