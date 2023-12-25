from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin  # , LoginRequiredMixin
from django.urls import reverse_lazy
# decorators:
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


class AdsList(PermissionRequiredMixin, ListView):
    # raise_exception = True
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
    # raise_exception = True
    permission_required = ('adboard.view_ad',)
    model = Ad
    template_name = 'ad.html'
    context_object_name = 'ad'


# ? список всех не имеет смысла, либо всех "своих" (к другим), либо всех "на свои" объявления, либо на конкретное...
# ? 3 списка делать?..
class ResponsesList(PermissionRequiredMixin, ListView):
    # raise_exception = True
    permission_required = ('adboard.view_response',)
    model = Response
    # queryset = Response.objects.filter(hidden=False, ).order_by('-creation_date')  # для ad_id=ad_id
    ordering = '-creation_date'
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 20


class AdCreate(PermissionRequiredMixin, CreateView):
    # raise_exception = True
    permission_required = ('adboard.add_ad', )
    form_class = AdForm
    model = Ad
    template_name = 'ad_edit.html'
    success_url = reverse_lazy('ads_list')


class AdEdit(PermissionRequiredMixin, UpdateView):
    # raise_exception = True
    permission_required = ('adboard.edit_ad', )
    form_class = AdForm
    model = Ad
    template_name = 'ad_edit.html'
    success_url = reverse_lazy('ads_list')


class AdDelete(PermissionRequiredMixin, DeleteView):
    # raise_exception = True
    permission_required = ('adboard.delete_ad', )
    model = Ad
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('ads_list')
