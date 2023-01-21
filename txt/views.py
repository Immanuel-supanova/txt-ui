import os
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, FormView

from txt.forms import DocumentForm, UploadDocumentForm
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


class TextCreateView(LoginRequiredMixin, CreateView):
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


class TextUpdateView(LoginRequiredMixin, UpdateView):
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
    txt.delete()
    return redirect('home')


class TextDetailView(LoginRequiredMixin, DetailView):
    template_name = "txt/detail_txt.html"
    model = TextDocument


class UploadFormView(LoginRequiredMixin, FormView):
    template_name = "txt/upload_txt.html"
    form_class = UploadDocumentForm

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        file = request.FILES['upload']
        split_tup = os.path.splitext(file.name)
        file_name = split_tup[0]

        if form.is_valid():
            user = User.objects.get(id=self.request.user.id)

            txt = file.read()

            text = TextDocument(title=f'{file_name}', content=txt.decode("utf-8"), author=user)
            text.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('home')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "txt/home.html"

    def get_context_data(self, **kwargs):
        # ___________________________________________________________

        context = super().get_context_data(**kwargs)

        context['documents'] = TextDocument.objects.filter(author=self.request.user.id)

        return context
