from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import ActionLog
# Create your views here.

@login_required
def action_logs_list(request):
    logs = ActionLog.objects.all()
    count_logs = ActionLog.objects.all().count()
    return render(request, 'action_log/action_log_list.html', {
        'logs': logs,
        'count_logs': count_logs
    })
