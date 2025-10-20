from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Member
from .forms import MemberForm

# Create your views here.

@login_required
def member_list(request):
    members = Member.objects.prefetch_related('courses')
    return render(request, 'member/member_list.html', {'members': members})

@login_required
def create_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            return redirect('members_app:member_list')
    else:
        form = MemberForm(request.GET)
    return render(request,'member/create_member.html', {'form': form})

@login_required
def update_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
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
        member.delete()
        return redirect('members_app:member_list')
    else:
        return render(request, 'member/member_confirm_delete.html', {'member': member})