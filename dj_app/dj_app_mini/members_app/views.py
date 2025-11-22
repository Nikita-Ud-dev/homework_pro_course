from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from members_app.models import Member
from members_app.forms import MemberForm
from courses_app.utils import get_logs
from accounts.current_user import set_current_user

# Create your views here.

@login_required
def member_list(request):
    members = Member.objects.prefetch_related('courses')
    return render(request, 'member/member_list.html', {'members': members})

@login_required
def create_member(request):
    if request.method == 'POST':
        set_current_user(request.user)
        form = MemberForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            return redirect('members_app:member_list')
    else:
        form = MemberForm()
    return render(request,'member/create_member.html', {'form': form})

@login_required
def update_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        set_current_user(request.user)
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('members_app:member_list')
    else:
        form = MemberForm(instance=member)
    return render(request,'member/update_member.html', {'form': form})

@login_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        set_current_user(request.user)
        member.delete()
        return redirect('members_app:member_list')
    else:
        return render(request, 'member/member_confirm_delete.html', {'member': member})

@login_required
def history_member_logs(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    logs = get_logs(member)
    count_logs = logs.count()
    return render(request, 'member/history_logs.html', {
        'logs': logs,
        'count_logs': count_logs,
    })


class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    template_name = 'member/member_list.html'
    context_object_name = 'members'
    admin_only = False
    white_list = ['l1x@example.com']

    def get_queryset(self):
        queryset = super().get_queryset().all()
        if self.request.user.is_superuser and self.admin_only and self.request.user.email in self.white_list:
            return queryset
        return queryset.filter(creator=self.request.user)


class AdminMemberListView(MemberListView):
    admin_only = True
    can_edit = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['can_edit'] = self.can_edit
        return context


class UserMemberListView(MemberListView):
    pass


class MemberCreateView(LoginRequiredMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'member/create_member.html'
    success_url = reverse_lazy('members_app:members_list_cbv')

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


class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    pk_url_kwarg = 'member_id'
    form_class = MemberForm
    template_name = 'member/update_member.html'
    success_url = reverse_lazy('members_app:members_list_cbv')

    def get_queryset(self):
        return Member.objects.filter(creator=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        set_current_user(request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['creator'] = self.request.user
        return form_kwargs


class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    pk_url_kwarg = 'member_id'
    template_name = 'member/member_confirm_delete.html'
    success_url = reverse_lazy('members_app:members_list_cbv')

    def dispatch(self, request, *args, **kwargs):
        set_current_user(request.user)
        return super().dispatch(request, *args, **kwargs)

class MemberHistoryLogsView(LoginRequiredMixin, DetailView):
    model = Member
    pk_url_kwarg = 'member_id'
    template_name = 'member/history_logs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        member = get_object_or_404(Member, id=self.object.pk)
        logs = get_logs(member)

        context['logs'] = logs
        context['count_logs'] = logs.count()
        return context