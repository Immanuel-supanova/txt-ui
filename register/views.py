from django.contrib.auth import get_user_model
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm

User = get_user_model()


class UserCreateView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "auth/signup.html"

    def get_success_url(self, *args, **kwargs):  # use this to direct to its immediate detail view
        return reverse_lazy('home')


def bad_request_view(request, exception):
    return render(request, '400.html', status=400)


def access_denied_view(request, exception):
    return render(request, '403.html', status=403)


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def internal_server_view(request):
    return render(request, '500.html', status=500)
