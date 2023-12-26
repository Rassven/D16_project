from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Author(User):
    # Основные
    # User fields: password, last_login (Дата и время последней активности в веб-приложении), username(unique),
    # first_name, last_name, email, is_staff (может заходить на панель администратора), is_active (доступ пользователя
    # на сайт в целом), date_joined (дата и время регистрации пользователя)
    auth_code = models.CharField(max_length=32, null=True, blank=True, default='12345678',
                                 verbose_name=_('Authorization code'))
    # Личная информация
    view_my_info = models.BooleanField(default=False, verbose_name=_('Viewing personal information'))
    # Всегда видны: username, date_joined, view_counter
    # для своей выделенная 'accounts/my_page' Для чужих 'accounts/users/<int:pk>'
    surname = models.CharField(max_length=32, null=True, blank=True, verbose_name=_('Surname'))  # Отчество
    b_day = models.DateTimeField(null=True, blank=True, verbose_name=_('Birthday'))  # "день рождения" (дата рождения)
    sex = models.IntegerField(choices=[(0, _('woman')), (1, _('man')), (2, _('undefined'))], default=2)
    # рассылки
    m_mailing = models.BooleanField(default=False, verbose_name=_('Mailing'))  # разрешить рассылку на e-mail
    view_counter = models.IntegerField(default=0, verbose_name=_('Profile views'))  # просмотры профиля

    def view_increment(self):  # пока все
        self.view_counter += 1
        self.save()
        return self.view_counter

    # @auth_finish.setter
    # def auth_finish(self, code):  # if auth_code
    #    if self.auth_code == code:
    #       self.auth_code = null
    #       self.save()
    #       return f'Поздравляем! Процедура авторизации завершена.'  # _('Authorisation complete')
    #    else:
    #       self.try_counter -= 1  # ? действие при =0
    #       self.save()
    #       return f'Неверный код! У вас осталось {self.try_counter} попыток. Будьте внимательны.'

    def __str__(self):
        return f'<{self.username} ({self.email})>'


class Ad(models.Model):
    C_LIST = [('tanks', 'Танки'), ('heals', 'Хилы'), ('dd', 'ДД'), ('buyers', 'Торговцы'),
              ('gld_masters', 'Гилдмастеры'), ('qst_givers', 'Квестгиверы'), ('smiths', 'Кузнецы'),
              ('tanners', 'Кожевники'), ('ptn_brewers', 'Зельевары'), ('spl_masters', 'Мастера заклинаний')]
    # Основные
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Ad created at..'))
    title = models.CharField(max_length=255, unique=True, null=False, verbose_name=_('Ad title'))
    text = models.TextField(null=False, verbose_name=_('Ad context'))  # нужно поле upload
    # upload = models.FileField(upload_to="uploads/", verbose_name=_('Ad upload'))
    category = models.CharField(max_length=32, choices=C_LIST, null=False,
                                default='tanks', verbose_name=_('Ad category'))
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE, verbose_name=_('Ad author'))
    # on_delete=models.SET_NULL, null=True

    # Дополнительные
    last_edit_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Ad last edit'))
    view_counter = models.IntegerField(default=0, verbose_name=_('Ad views'))

    def view_increment(self):
        self.view_counter += 1
        self.save()
        return self.view_counter

    def __str__(self):
        return f'{self.author.username} {self.title[:24]}...'

    def get_absolute_url(self):
        return reverse('ad', args=[str(self.id)])


class Response(models.Model):
    # Основные
    creation_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=255, null=False, verbose_name=_('Response content'))
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE, verbose_name=_('Response author'))
    ad = models.ForeignKey(to='Ad', on_delete=models.CASCADE, verbose_name=_('Response to ad'))
    # Дополнительные
    last_edit_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Last edited response'))
    # auto_now приемлемо?
    hidden = models.BooleanField(default=False, verbose_name=_('Response visibility'))
    status = models.IntegerField(
        choices=[(0, _('Just exists')), (1, _('Is read')), (2, _('Accepted')), (-1, _('Rejected'))],
        default=0, verbose_name=_('Response status'))
    # (кнопки) действия ("одно из") в шаблоне: "принять" status = 2, "отклонить" status = -1,
    # "отменить действия" status = 1, !!!вернуться к status = 0 нельзя. При =1 кнопка отмены пассивна.

    def __str__(self):
        return f'{self.text[:20]} ({self.author.username}) to {self.ad.title[:24]} ({self.ad.author.username})'
