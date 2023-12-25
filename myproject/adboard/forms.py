from django import forms
from django.core.exceptions import ValidationError
from .models import Author, Ad, Response


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        # fields = '__all__'  # на время тестирования
        fields = ['category', 'title', 'text', ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title is not None and len(title) < 2:
            raise ValidationError({"title": "Название не может быть менее 10 символов."})
        text = cleaned_data.get("text")
        if text == title:
            raise ValidationError("Текст не должен повторять название.")
        if title[0].islower():
            raise ValidationError("Название должно начинаться с заглавной буквы")
        return cleaned_data
        # IntegrityError at /adboard/ad/add/
        # NOT NULL constraint failed: adboard_ad.author_id


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = '__all__'  # на время тестирования
        # fields = ['category', 'title', 'text', 'hidden']
