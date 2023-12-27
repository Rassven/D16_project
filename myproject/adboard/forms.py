from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Author, Ad, Response


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'title', 'text', ]


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        # Response.author = forms.ModelChoiceField(label='Author', queryset=Author.objects.get(id=Author.id))
        # Response.author = forms.ModelChoiceField(label='Author', queryset=Author.objects.all())
        # Response.author = User.author
        fields = '__all__'  # на время тестирования
        # fields = ['text', 'hidden', ]  # 'ad' - auto, 'author' - auto (не работает, данные не передаются в форму)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data