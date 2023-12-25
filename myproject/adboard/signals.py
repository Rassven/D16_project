from myproject.mconfig import config
from django.db.models.signals import post_save
# Еще сигналы (django.db.models.signals./ИМЯ/):
# pre_save, post_save — вызываются до и после вызова save() метода модели;
# pre_delete и post_delete — вызываются до и после вызова delete() метода модели или набора объектов (queryset);
# m2m_changed — вызывается, когда ManyToManyField в модели изменяется;
# request_started и request_finished — вызывается перед и после обработки HTTP-запроса.
# Документация по сигналам: https://docs.djangoproject.com/en/4.0/ref/signals/
from django.dispatch import receiver
from .models import *

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

# @receiver(post_save, sender=Ad)
# def ad_created(instance, **kwargs):
#     print('Создано объявление', instance)


@receiver(post_save, sender=Ad)
def ad_created(instance, created, **kwargs):
    if not created:
        return
    # print('Creation!')
    emails = User.objects.values_list('email', flat=True)  # пока без filter(...instance.category)
    subject = f'Новое объявление'
    text_content = (
        f'Объявление: {instance.title} от {instance.author.username}\n'
        f'В категории {instance.category}. Размещено: {instance.creation_date}\n\n'
        f'Кратко: {instance.text[:30]}. Ознакомиться: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Объявление: {instance.title} от {instance.author.username}<br>'
        f'В категории {instance.category}. Размещено: {instance.creation_date}<br><br>'
        f'Кратко: {instance.text[:30]}. <a href="http://127.0.0.1{instance.get_absolute_url()}">Ознакомиться</a>'
    )
    # Ссылка из почты не работает (локальный сервер?)!!!
    print('Sending emails...')
    for email in emails:
        print(email)
        msg = EmailMultiAlternatives(subject, text_content, None, [config['ctrl_mail'], ])  # + email !
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=Response)
def ad_created(instance, created, **kwargs):
    if not created:
        return
    # print('Creation!')
    emails = User.objects.values_list('email', flat=True)  # пока без filter(...instance.category и прочих)
    subject = f'Новый отклик'
    text_content = (
        f'Отклик на {instance.ad.title} ({instance.author.username}) от {instance.creation_date}\n\n'
        f'Кратко: {instance.text[:30]} Ознакомиться: http://127.0.0.1:8000{instance.get_absolute_url()}\n'
    )
    html_content = (
        f'Объявление: {instance.title} ({instance.author.username}) от {instance.creation_date}<br><br>'
        f'Кратко: {instance.text[:30]} Ознакомиться: http://127.0.0.1:8000{instance.get_absolute_url()}<br>'
    )
    # Ссылка из почты не работает (локальный сервер?)!!!
    print('Sending emails...')
    for email in emails:
        print(email)
        msg = EmailMultiAlternatives(subject, text_content, None, [config['ctrl_mail'], ])  # + email !
        msg.attach_alternative(html_content, "text/html")
        msg.send()
