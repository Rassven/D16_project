from django.shortcuts import render
from adboard.models import Author
from django.views.generic import ListView
# from django.contrib.auth.models import User
from django.views.generic.edit import CreateView  # , DeleteView
from .forms import SignUpForm


class MyPage(ListView):
    permission_required = ('user.auth', )
    model = Author
    template_name = 'mypage.html'
    context_object_name = 'author'


class SignUp(CreateView):
    model = Author
    form_class = SignUpForm
    success_url = '/accounts/signup/'
    template_name = 'registration/signup.html'


# class MyLogin(CreateView):
#     model = Author
#     form_class = SignUpForm
#     success_url = '/accounts/mylogin'
#     template_name = 'registration/login.html'
