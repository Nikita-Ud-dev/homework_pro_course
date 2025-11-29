from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import ActionLog
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from courses_app.mixins import SearchMultiFilterMixin
# Create your views here.

@login_required
def action_logs_list(request):
    logs = ActionLog.objects.all()
    count_logs = ActionLog.objects.all().count()
    return render(request, 'action_log/action_log_list.html', {
        'logs': logs,
        'count_logs': count_logs
    })

class LogListView(LoginRequiredMixin, PermissionRequiredMixin, SearchMultiFilterMixin, ListView):
    model = ActionLog
    template_name = 'action_log/action_log_list.html'
    context_object_name = 'logs'
    white_list = ['l1x@example.com']
    permission_required = 'accounts.view_actionlog'
    search_field = "Пошук логу по назві об'єкта:"
    search_name_field_list = ['name_object']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        logs = context['logs']
        context['count_logs'] = logs.count()
        return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if self.request.user.is_superuser and self.request.user.email in self.white_list:
    #         return queryset
    #     return queryset.filter(user=self.request.user)
