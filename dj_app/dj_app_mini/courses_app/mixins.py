from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.api import success
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from unicodedata import lookup

from accounts.models import ActionLog
from accounts.current_user import set_current_user
from courses_app.models import Course
from django.views.generic import CreateView, UpdateView, DeleteView


class AdditionalFormKwargMixin:
    form_kwarg = None
    form_kwarg_name = None
    add_user_to_form = True

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        if self.add_user_to_form:
            form_kwargs['creator'] = self.request.user
        if self.form_kwarg and self.form_kwarg_name:
            form_kwargs[self.form_kwarg_name] = self.form_kwarg
        return form_kwargs

class UserObjectFilterMixin:
    user_field = 'creator'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.model == Course:
            queryset = super().get_queryset().annotate(count_members=Count('list_of_members'))
        if not self.request.user.is_superuser:
            filter_kwargs = {self.user_field: self.request.user}
            queryset = queryset.filter(**filter_kwargs)
        return queryset


class SetUserMixin:
    def dispatch(self, request, *args, **kwargs):
        set_current_user(request.user)
        return super().dispatch(request, *args, **kwargs)

class CreateActionLogMixin:
    action_type = 'Створено'
    log_name_field = None

    def get_object_name(self, form):
        field = self.log_name_field
        if not field:
            return ''

        value = getattr(form.instance, field, '')

        if callable(value):
            return value()
        return value

    def form_valid(self, form):
        response = super().form_valid(form)
        object_name = self.get_object_name(form)

        ActionLog.objects.create(
            name_log = f'{self.model.__name__}',
            user = self.request.user,
            action_type = self.action_type,
            content_type = ContentType.objects.get_for_model(self.model),
            name_object = object_name,
            object_id = form.instance.id,
        )
        return response

class UpdateActionLogMixin:
    action_type = 'Оновленно'
    log_name_field = None

    def get_object_name(self, form):
        field = self.log_name_field
        if not field:
            return ''

        value = getattr(form.instance, field, '')

        if callable(value):
            return value()
        return value

    def form_valid(self, form):
        response = super().form_valid(form)
        object_name = self.get_object_name(form)

        ActionLog.objects.create(
            name_log = f'{self.model.__name__}',
            user = self.request.user,
            action_type = self.action_type,
            content_type = ContentType.objects.get_for_model(self.model),
            name_object = object_name,
            object_id = form.instance.id,
        )
        return response

class DeleteActionLogMixin:
    action_type = 'Видалено'
    log_name_field = None

    def get_object_name(self):
        field = self.log_name_field
        if not field:
            return ''

        value = getattr(self.object, field, '')

        if callable(value):
            return value()
        return value

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        object_name = self.get_object_name()
        object_id = self.object.id

        ActionLog.objects.create(
            name_log = f'{self.model.__name__}',
            user = self.request.user,
            action_type = self.action_type,
            content_type = ContentType.objects.get_for_model(self.model),
            name_object = object_name,
            object_id = object_id,
        )
        return super().post(request, *args, **kwargs)

class SuccessMessageFormMixin:
    success_message = f''
    message = False
    log_name_field = None

    def get_object_name_form(self, form):
        field = self.log_name_field
        if not field:
            return ''

        value = getattr(form.instance, field, '')

        if callable(value):
            return f"Людина '{value()}' "
        return f"Об'єкт '{value}' "

    def form_valid(self, form):
        response = super().form_valid(form)
        name_object = self.get_object_name_form(form)

        if self.message:
            messages.success(self.request, name_object + self.success_message)

        return response


class SuccessMessageDeleteMixin:
    success_message = f''
    message = False
    log_name_field = None

    def get_object_name_delete(self):
        field = self.log_name_field
        if not field:
            return ''

        value = getattr(self.object, field, '')

        if callable(value):
            return f"Людина '{value()}' "
        return f"Об'єкт '{value}' "

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        name_object = self.get_object_name_delete()

        if self.message:
            messages.success(self.request, name_object + self.success_message)

        return super().post(request, *args, **kwargs)

class SearchFilterMixin:
    search_name_field = None
    search_field = None

    def get_queryset(self):
        queryset = super().get_queryset()
        search_name_field = self.search_name_field
        search = self.request.GET.get('search')

        if not search:
            return queryset

        lookup_filter = f'{search_name_field}__icontains'
        queryset_filtered = queryset.filter(**{lookup_filter: search})

        return queryset_filtered

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')

        context['search'] = query
        context['search_field'] = self.search_field
        return context

class SearchMultiFilterMixin:
    search_name_field_list = []
    search_field = None

    def get_queryset(self):
        queryset = super().get_queryset()
        search_name_field_list = self.search_name_field_list
        search = self.request.GET.get('search')
        list_field = Q()
        if not search:
            return queryset

        for field in search_name_field_list:
            lookup_filter = f'{field}__icontains'
            list_field = list_field | Q(**{lookup_filter: search})

        queryset_filtered = queryset.filter(list_field)

        return queryset_filtered

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')

        context['search'] = query
        context['search_field'] = self.search_field
        return context