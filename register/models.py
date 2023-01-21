from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'
    PREFER = 'Prefer not to say'

    GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (PREFER, 'Prefer not to say'),

    ]

    slug = models.SlugField()
    gender = models.CharField(max_length=255, choices=GENDER)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Please enter a valid phone number")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)
    timestamp = models.TimeField(auto_now_add=True, blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.slug = self.username
        super(User, self).save(*args, **kwargs)
