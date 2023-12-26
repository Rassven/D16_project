from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin  # , LoginRequiredMixin
from django.urls import reverse_lazy
# from django.views.decorators.csrf import csrf_protect

# my app:
from .models import *
from .filters import AdFilter, ResponseFilter
from .forms import AdForm, ResponseForm


def start(request):
    print('Start page message: >>> Запущен сервер приложения. <<<')
    return render(request, 'welcome.html')


class RulesView(TemplateView):
    template_name = 'rules.html'


# Объявления
class AdsList(PermissionRequiredMixin, ListView):
    permission_required = ('adboard.view_ad',)
    model = Ad
    ordering = '-creation_date'  # лучше фильтрация на странице
    template_name = 'ads.html'
    context_object_name = 'ads'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AdView(PermissionRequiredMixin, DetailView):
    permission_required = ('adboard.view_ad',)
    model = Ad
    template_name = 'ad.html'
    context_object_name = 'ad'


class AdCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('adboard.add_ad', )
    form_class = AdForm
    model = Ad
    template_name = 'ad_edit.html'
    success_url = reverse_lazy('ads_list')


class AdEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('adboard.edit_ad', )
    form_class = AdForm
    model = Ad
    template_name = 'ad_edit.html'
    success_url = reverse_lazy('ads_list')


class AdDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('adboard.delete_ad', )
    model = Ad
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('ads_list')


# Отклики
class ResponsesList(PermissionRequiredMixin, ListView):
    permission_required = ('adboard.view_response',)
    model = Response
    # queryset = Response.objects.filter(hidden=False, ad_id...).order_by('-creation_date')  # для ad_id=ad_id
    ordering = '-creation_date'
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 20


class ResponseView(PermissionRequiredMixin, DetailView):
    permission_required = ('adboard.view_response',)
    model = Response
    template_name = 'response.html'
    context_object_name = 'response'


class ResponseCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('adboard.add_response', )
    form_class = ResponseForm
    model = Response
    template_name = 'response_edit.html'
    success_url = reverse_lazy('responses_list')


class ResponseEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('adboard.edit_response', )
    form_class = AdForm
    model = Response
    template_name = 'response_edit.html'
    success_url = reverse_lazy('responses_list')


class ResponseDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('adboard.delete_response', )
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('responses_list')
