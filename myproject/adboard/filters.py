from django_filters import FilterSet, DateTimeFilter  # , ModelChoiceFilter
from django.forms import DateTimeInput
from .models import Author, Ad, Response
from django.utils.translation import gettext_lazy as _


class AdFilter(FilterSet):
    creation_date = DateTimeFilter(field_name=_('creation_date'), lookup_expr='gte',
                                   widget=DateTimeInput(format='%Y-%m-%d', attrs={'type': 'datetime-local'}, ), )

    class Meta:
        model = Ad
        fields = {
            'author': ['exact'],
            'category': ['exact'],
            'title': ['icontains'],
            'creation_date': ['lte', 'gte'],
       }


class ResponseFilter(FilterSet):
    class Meta:
        model = Response
        fields = {
            'author': ['exact'],
            'creation_date': ['lte', 'gte'],
            # 'status': ['icontains'],
        }
