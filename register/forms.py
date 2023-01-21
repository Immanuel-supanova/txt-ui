from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, \
    PasswordResetForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="Firstname", widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Lastname", widget=forms.TextInput(attrs={"class": "form-control"}))

    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"class": "form-control"}))
    phone_number = forms.CharField(label="Phone number(optional)",
                                   widget=forms.TextInput(attrs={"class": "form-control"}), required=False)

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "gender", "phone_number", "email")
        widgets = {
            'gender': forms.Select(attrs={"class": "form-control"}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_details = User.objects.filter(username=username)
        if user_details.exists():
            raise forms.ValidationError("Username is already taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_details = User.objects.filter(email=email)
        if user_details.exists():
            raise forms.ValidationError("There is already an account with this email , please try logging in!")
        return email


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control"}),
    )


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, "class": "form-control"}),
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
    )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "form-control"}),
    )
