from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Count
from courses_app.models import Course, Teacher
from courses_app.forms import CourseForm, TeacherForm
from courses_app.utils import get_logs
from accounts.current_user import set_current_user
from accounts.models import ActionLog
# Create your views here.

# User = get_user_model()

@login_required
def course_list(request):
    count_member = Course.objects.annotate(count_members=Count('list_of_members'))
    return render(request, 'course/course_list.html', {'courses': count_member})

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

@login_required
def history_course_logs(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    logs = get_logs(course)
    count_logs = logs.count()
    return render(request, 'course/history_logs.html', {
        'logs': logs,
        'count_logs': count_logs,
    })

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'course/course_list.html'
    context_object_name = 'courses'
    admin_only = False
    white_list = ['l1x@example.com']

    def get_queryset(self):
        queryset_courses = super().get_queryset().annotate(count_members=Count('list_of_members'))
        if self.request.user.is_superuser and self.admin_only and self.request.user.email in self.white_list:
            return queryset_courses
        return queryset_courses.filter(creator=self.request.user)

class AdminCourseListView(CourseListView):
    admin_only = True
    can_edit = False

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data()
        context['can_edit'] = self.can_edit
        return context

class UserCourseListView(CourseListView):
    pass

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/create_course.html'
    success_url = reverse_lazy('courses_app:courses_list_cbv')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['creator'] = self.request.user
        return form_kwargs

    def dispatch(self, request, *args, **kwargs):
        set_current_user(request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    pk_url_kwarg = 'course_id'
    form_class = CourseForm
    template_name = 'course/update_course.html'
    success_url = reverse_lazy('courses_app:courses_list_cbv')

    def get_queryset(self):
        return Course.objects.filter(creator=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        set_current_user(request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['creator'] = self.request.user
        return form_kwargs

class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    pk_url_kwarg = 'course_id'
    template_name = 'course/course_confirm_delete.html'
    success_url = reverse_lazy('courses_app:courses_list_cbv')

    def dispatch(self, request, *args, **kwargs):
        set_current_user(request.user)
        return super().dispatch(request, *args, **kwargs)

class CourseHistoryLogsView(LoginRequiredMixin, DetailView):
    model = Course
    pk_url_kwarg = 'course_id'
    template_name = 'course/history_logs.html'
    # context_object_name = 'logs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        course = get_object_or_404(Course, id=self.object.pk)
        logs = get_logs(course)

        context['logs'] = logs
        context['count_logs'] = logs.count()
        return context
        # course1 = self.object
        # model_class = self.object.__class__
        # logs = ActionLog.objects.filter(
        #     content_type = ContentType.objects.get_for_model(model_class),
        #     object_id = course.pk
        # )

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

@login_required
def history_teacher_logs(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    logs = get_logs(teacher)
    count_logs = logs.count()
    return render(request, 'teacher/history_logs.html', {
        'logs': logs,
        'count_logs': count_logs,
    })

class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = 'teacher/teacher_list.html'
    context_object_name = 'teachers'
    admin_only = False
    white_list = ['l1x@example.com']

    def get_queryset(self):
        queryset = super().get_queryset().all()
        if self.request.user.is_superuser and self.admin_only and self.request.user.email in self.white_list:
            return queryset
        return queryset.filter(creator=self.request.user)

class AdminTeacherListView(TeacherListView):
    admin_only = True
    can_edit = False

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data()
        context['can_edit'] = self.can_edit
        return context

class UserTeacherListView(TeacherListView):
    pass

class TeacherCreateView(LoginRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teacher/create_teacher.html'
    success_url = reverse_lazy('courses_app:teachers_list_cbv')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['creator'] = self.request.user
        return form_kwargs

    def dispatch(self, request, *args, **kwargs):
        set_current_user(request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    model = Teacher
    pk_url_kwarg = 'teacher_id'
    form_class = TeacherForm
    template_name = 'teacher/update_teacher.html'
    success_url = reverse_lazy('courses_app:teachers_list_cbv')

    def get_queryset(self):
        return Teacher.objects.filter(creator=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        set_current_user(request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['creator'] = self.request.user
        return form_kwargs

class TeacherDeleteView(LoginRequiredMixin, DeleteView):
    model = Teacher
    pk_url_kwarg = 'teacher_id'
    template_name = 'teacher/teacher_confirm_delete.html'
    success_url = reverse_lazy('courses_app:teachers_list_cbv')

    def dispatch(self, request, *args, **kwargs):
        set_current_user(request.user)
        return super().dispatch(request, *args, **kwargs)

class TeacherHistoryLogsView(LoginRequiredMixin, DetailView):
    model = Teacher
    pk_url_kwarg = 'teacher_id'
    template_name = 'teacher/history_logs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        teacher = get_object_or_404(Teacher, id=self.object.pk)
        logs = get_logs(teacher)

        context['logs'] = logs
        context['count_logs'] = logs.count()
        return context