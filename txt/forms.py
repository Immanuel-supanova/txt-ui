from django import forms

from .models import TextDocument


class DocumentForm(forms.ModelForm):
    class Meta:
        model = TextDocument
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'File Name e.g untitled'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UploadDocumentForm(forms.Form):
    upload = forms.FileField(widget=forms.FileInput)
