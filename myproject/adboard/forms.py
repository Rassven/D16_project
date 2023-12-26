from django import forms
from django.core.exceptions import ValidationError
from .models import Author, Ad, Response


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'title', 'text', ]


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = '__all__'  # на время тестирования
        # fields = ['category', 'title', 'text', 'hidden']
