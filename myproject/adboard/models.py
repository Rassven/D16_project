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
    # avatar = models.ImageField(/path/)  # как идет разграничение доступа к файлам? По имени?
    # рассылки
    m_mailing = models.BooleanField(default=False, verbose_name=_('Mailing'))  # разрешить рассылку на e-mail
    # f_mailing = models.CharField(max_length=64,choices=[
    #     ('message', _('Short message')), ('push', _('Push message')), ('disable', _('Disable')), ],
    #                              default='disable',
    #                              verbose_name=_('Phone mailing'))
    # mailing_period = models.IntegerField(default=7, verbose_name=_('Notify period (days)'))
    # mailing_week_day = models.IntegerField(choices=[
    #     (0, _('Every day')), (1, _('Monday')), (2, _('Tuesday')), (3, _('Wednesday')),
    #     (4, _('Thursday')), (5, _('Friday')), (6, _('Saturday')), (7, _('Sunday'))],
    #     default=0, verbose_name=_('Notify week day'))
    # ?связать "дней" и "день недели"..
    view_counter = models.IntegerField(default=0, verbose_name=_('Profile views'))  # просмотры профиля

    # метод инкремента просмотров (? считать все попытки, или по числу пользователей (нужен список тех кто уже..)
    def view_increment(self):
        self.view_counter += 1
        self.save()
        return self.view_counter

    # @auth_finish.setter  # если использовать обращение к конкретному полю модели (не к ней в целом) как "сигнал"?..
    # def auth_finish(self, code):  # if auth_code
    #    if self.auth_code = code:
    #       self.auth_code = null
    #       self.save()
    #       return f'Поздравляем! Процедура авторизации завершена.'  # _('Authorisation complete')
    #    else:
    #       self.try_counter -= 1  # =0 и? Удалить модель автора?
    #       self.save()
    #       return f'Неверный код! У вас осталось {self.try_counter} попыток. Будьте внимательны.'

    def __str__(self):  # все же следует указать, чисто для удобства в админке, в шаблонах он н.не нужен.
        return f'<{self.username} ({self.email})>'


class Ad(models.Model):
    C_LIST = [('tanks', 'Танки'), ('heals', 'Хилы'), ('dd', 'ДД'), ('buyers', 'Торговцы'),
              ('gld_masters', 'Гилдмастеры'), ('qst_givers', 'Квестгиверы'), ('smiths', 'Кузнецы'),
              ('tanners', 'Кожевники'), ('ptn_brewers', 'Зельевары'), ('spl_masters', 'Мастера заклинаний')]
    # Основные
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Ad created at..'))
    title = models.CharField(max_length=255, unique=True, null=False, verbose_name=_('Ad title'))
    text = models.TextField(null=False, verbose_name=_('Ad context'))  # нужно поле upload (? текстовую часть туда же?)
    # upload = models.FileField(upload_to="uploads/", verbose_name=_('Ad upload'))
    category = models.CharField(max_length=32, choices=C_LIST, null=False,
                                default='tanks', verbose_name=_('Ad category'))
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE, verbose_name=_('Ad author'))
    # on_delete=models.SET_NULL, null=True

    # Дополнительные
    last_edit_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Ad last edit'))
    view_counter = models.IntegerField(default=0, verbose_name=_('Ad views'))
    # принцип работы? По каждому открыванию? Если один и тот же пользователь?.. !Кроме своих посещений!
    # reply_counter = models.IntegerField(default=0, verbose_name=_('Ad replys'))  # ?"счетчик" ?а оно надо?
    # notify = models.IntegerField(default=0, verbose_name=_('Change notify flag'))
    # если не 0, то равен разнице в reply_counter (разнице с чем?) ?Хранить старое значение до сброса notify?

    def view_increment(self):  # При открытии на чтение (кроме собственного!).
        self.view_counter += 1
        self.save()
        return self.view_counter

    # def reply_count(self):  # может совместить с получением списка откликов?
    #     # if Response.objects.all().exists()  # если Response (вообще) не пустой... ?? И что считаем?
    #     #       # ad_responses = Response.objects.filter(response__ad_id=ad_id)  # список с нужным id
    #     #       self.reply_counter = ad_responses.count()  # проверить!
    #     #       self.reply_counter = self.response_set.count()  # проверить!
    #             self.save()
    #     return self.reply_counter  # ad_responses  # а считать уже в шаблоне?

    def __str__(self):  # следует указать, чисто для удобства в админке, в шаблонах он н.не нужен.
        return f'{self.author.username} {self.title[:24]}...'

    def get_absolute_url(self):
        return reverse('ad', args=[str(self.id)])

    # !!! пометка, если отредактировано с id отличным от "авторского"!


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
    # (флажок в форме создания (и в форме изменения тоже)) невидимость (видны только авторам объявления и отклика)
    # для посторонних
    status = models.IntegerField(
        choices=[(0, _('Just exists')), (1, _('Is read')), (2, _('Accepted')), (-1, _('Rejected'))],
        default=0, verbose_name=_('Response status'))
    # status = 0 - просто существует (не открывалось), 1 - обращение (показ) без действия = "прочитано",
    # (кнопки) действия ("одно из") в шаблоне: "принять" status = 2, "отклонить" status = -1,
    # "отменить действия" status = 1, !!!вернуться к status = 0 нельзя. При =1 кнопка отмены пассивна.

    def __str__(self):  # следует указать, чисто для удобства в админке, в шаблонах он н.не нужен.
        return f'{self.text[:20]} ({self.author.username}) to {self.ad.title[:24]} ({self.ad.author.username})'

    # !!! пометка, если отредактировано с id отличным от "авторского"!
