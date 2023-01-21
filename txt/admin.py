from django.contrib import admin

from .forms import DocumentForm
from .models import TextDocument


# Register your models here.

class TextModelAdmin(admin.ModelAdmin):
    form = DocumentForm


admin.site.register(TextDocument, TextModelAdmin)
