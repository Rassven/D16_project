# from project.mconfig import config
from django import forms
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django.core.mail import send_mail, mail_admins, EmailMultiAlternatives  # , mail_managers
from adboard.models import Author


class SignUpForm(UserCreationForm):
    class Meta:
        model = Author
        fields = ("username", 'view_my_info')  # , "email")

    def save(self, request):  # request? SignUpForm.save() missing 1 required positional argument: 'request'
        print(request.data, request.user)
        user = super().save(request)
        return user


# Добавление в группы при регистрации. Рассылка писем
class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        authors_group = Group.objects.get(name="Authors")
        user.groups.add(authors_group)
#         # send_mail(subject='Добро пожаловать на "доску объявлений"!',
#         #     message=f'{user.username}, вы успешно зарегистрировались! ({request.get_host()})',
#         #     from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
#         #     recipient_list=[user.email], )
        subject = 'Добро пожаловать на сайт Доска Объявлений!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте (host: ({request.get_host()}))!'
        text += f'Ваш пароль для окончания регистрации: {user.auth_code}'
        html = (f'<b>{user.username}</b>, вы успешно зарегистрировались на '
                f'<a href="http://127.0.0.1:8000/">сайте</a> (host: {request.get_host()}, '
                f'user.date_joined: {user.date_joined})!'
                f'Ваш пароль для окончания регистрации: {user.auth_code}')
        # msg = EmailMultiAlternatives(subject=subject, body=text, from_email=None, to=[user.email])
        msg = EmailMultiAlternatives(subject=subject, body=text, from_email=None, to=[config['ctrl_mail'], ])
        msg.attach_alternative(html, "text/html")
        msg.send()
        # mail_managers(subject='[M] Новенький!',
        #             # message=f'[M] {user.username} в {user.date_joined} зарегистрировался на сайте.')
        mail_admins(subject='[A] Новенький!',
                    message=f'[A] {user.username} в {user.date_joined}  зарегистрировался на сайте.')
        return user
