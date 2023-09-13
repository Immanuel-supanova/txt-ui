# Mixins for TextDocument model
import os

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from txt.models import TextDocument

User = get_user_model()


class TextCreateMixin(UserPassesTestMixin):

    def form_valid(self, form):
        response = super().form_valid(form)
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.model).pk,
            object_id=self.object.pk,
            object_repr=self.object.title,
            action_flag=ADDITION)
        return response

    def test_func(self):
        return self.request.user.has_perm('add_textdocument')


class TextUploadMixin(UserPassesTestMixin):

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        file = request.FILES['upload']
        split_tup = os.path.splitext(file.name)
        file_name = split_tup[0]

        if form.is_valid():
            response = self.form_valid(form)
            user = User.objects.get(id=self.request.user.id)

            txt = file.read()

            text = TextDocument(title=f'{file_name}', content=txt.decode("utf-8"), author=user)
            text.save()
            LogEntry.objects.log_action(
                user_id=self.request.user.id,
                content_type_id=ContentType.objects.get_for_model(TextDocument).pk,
                object_id=text.id,
                object_repr=text.title,
                action_flag=ADDITION)
            return response
        else:
            return self.form_invalid(form)

    def test_func(self):
        return self.request.user.has_perm('add_textdocument')


class TextUpdateMixin(UserPassesTestMixin):

    def form_valid(self, form):
        response = super().form_valid(form)
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.model).pk,
            object_id=self.object.pk,
            object_repr=self.object.title,
            action_flag=CHANGE)
        return response

    def test_func(self):
        return self.request.user.has_perm('change_textdocument')


class TextDeleteMixin(UserPassesTestMixin):

    def form_valid(self, form):
        success_url = self.get_success_url()
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(self.model).pk,
            object_id=self.object.id,
            object_repr=self.object.title,
            action_flag=DELETION)
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def test_func(self):
        return self.request.user.has_perm('delete_textdocument')


class TextViewMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm('view_textdocument')
