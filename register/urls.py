from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordResetView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy

from .forms import LoginForm, UserPasswordChangeForm, UserPasswordResetForm
from .views import UserCreateView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name="user-create"),
    path('login/', LoginView.as_view(template_name="auth/login.html", form_class=LoginForm), name="login"),
    path('logout/', LogoutView.as_view(template_name="auth/logged_out.html"), name="logout"),
    path(
        "password_change/",
        PasswordChangeView.as_view(template_name="auth/password_change_form.html", form_class=UserPasswordChangeForm),
        name="password_change"
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(template_name="auth/password_change_done.html"),
        name="password_change_done",
    ),
    path('password_reset/', PasswordResetView.as_view(from_email=settings.DEFAULT_FROM_EMAIL,
                                                      email_template_name="auth/email/password_reset_email.html",
                                                      subject_template_name="auth/email/password_reset_subject.html",
                                                      success_url=reverse_lazy("password_reset_done"),
                                                      template_name="auth/password_reset_form.html",
                                                      form_class=UserPasswordResetForm),
         name='password_reset_done'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="auth/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
         name='password_reset_complete'),

]
