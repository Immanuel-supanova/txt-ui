import re

from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView, FormView

from txt.forms import DocumentForm, UploadDocumentForm
from txt.mixins import TextCreateMixin, TextUpdateMixin, TextViewMixin, TextUploadMixin
from txt.models import TextDocument

User = get_user_model()

today = timezone.now()
# as per recommendation from @freylis, compile once only
cleanr = re.compile('<.*?>')


def cleanhtml(raw_html):
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


# Create your views here.

def download_txt(request, pk):
    text = TextDocument.objects.filter(id=pk)

    response = HttpResponse(content_type='text/plain')
    lines = []
    for texts in text:
        response['content-disposition'] = f'attachment; filename = {texts.name()}'
        lines.append(cleanhtml(texts.content))

    response.writelines(lines)
    return response


class TextCreateView(LoginRequiredMixin, TextCreateMixin, CreateView):
    template_name = "txt/create_txt.html"
    model = TextDocument
    form_class = DocumentForm

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.author = User.objects.get(id=self.request.user.id)
        blog.save()
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):  # use this to direct to its immediate detail view
        return reverse_lazy('txt-detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        context_p = User.objects.all()
        return context_p

    def get_context_data(self, **kwargs):
        # ___________________________________________________________

        context = super().get_context_data(**kwargs)

        context['user'] = User.objects.filter(id=self.request.user.id)

        return context


class TextUpdateView(LoginRequiredMixin, TextUpdateMixin, UpdateView):
    template_name = "txt/update_txt.html"
    model = TextDocument
    form_class = DocumentForm

    def form_valid(self, form):
        txt = form.save(commit=False)
        txt.date_modified = today
        txt.save()
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):  # use this to direct to its immediate detail view
        return reverse_lazy('txt-detail', kwargs={'pk': self.object.pk})


def text_delete_view(request, pk):
    txt = TextDocument.objects.get(id=pk)
    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(TextDocument).pk,
        object_id=txt.id,
        object_repr=txt.title,
        action_flag=DELETION)
    txt.delete()
    return redirect('home')


class TextDetailView(LoginRequiredMixin, TextViewMixin, DetailView):
    template_name = "txt/detail_txt.html"
    model = TextDocument


class UploadFormView(LoginRequiredMixin, TextUploadMixin, FormView):
    template_name = "txt/upload_txt.html"
    form_class = UploadDocumentForm

    def get_queryset(self):
        context_p = User.objects.all()
        return context_p

    def get_context_data(self, **kwargs):
        # ___________________________________________________________

        context = super().get_context_data(**kwargs)

        context['user'] = User.objects.filter(id=self.request.user.id)

        return context

    def get_success_url(self, *args, **kwargs):  # use this to direct to its immediate detail view
        return reverse_lazy('home')
