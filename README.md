# Txt-ui

Txt-ui is a django application for creating, updating, uploading, deleting text document. The content and the title of the documents are stored in a database when needed as a txt file you can download them.


To install the application write the following command

```commandline
pip install git+https://github.com/Immanuel-supanova/txt-ui.git
```
Add the following lines of code in your project settings.py file

```
INSTALLED_APPS = [
    'txt',

    'django_bootstrap5',
    'django_cleanup.apps.CleanupConfig',
    'ckeditor',

]
```
```
# ckeditor settings
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'height': '475',
        'width': '1225',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['Styles', 'Format', 'Font', 'FontSize']
        ]
    },
}

```

```
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media/'
```

The following line of code is very important because the views in txt app use 'LoginRequiredMixin', so you must have an established authentication
if not you can use the admin authentication system

```
LOGIN_URL = 'admin:login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

In your command line interface that you use, write the following commands to complete the setup
```commandline
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


If you want to use the txt demo app, in the urls.py file in the root directory add the following:

```
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('txtapp.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

settings.py:
```
INSTALLED_APPS = [
    'txtapp',
]
```