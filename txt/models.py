from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


# Create your models here.
class TextDocument(models.Model):
    title = models.CharField(max_length=250)
    content = RichTextField(config_name='awesome_ckeditor')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    def name(self):
        return f'{self.title}.txt'

    def __str__(self):
        return self.name()

    """def delete(self, *args, **kwargs):
        # first, delete the file
        self.text.delete(save=False)"""
