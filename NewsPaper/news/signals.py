from django.shortcuts import render
from django.utils import timezone
from requests import request
from datetime import datetime, timedelta
from .models import *
from .tasks import *
from allauth.account.signals import user_signed_up
from django.template.loader import render_to_string
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives

# если произошло добавление новости, то подписанным пользователям отправляем письма
@receiver(m2m_changed, sender=Post.categories.through)
# m2m_changed возникает при изменении ManyToManyField модели.
def send_mail_on_post(sender, action, instance, **kwargs):
    # отправляем письмо
    if action == 'post_add':  # если событие добавление поста
        cats = instance.categories.all()  # берем все категории
        for c in cats:  # цикл по всем категориям
            users = c.subscribers.all()  # бежим по связям, пользователей, которые подписаны на категории новостей, собираем этих пользователей
            for u in users:
                task_mail_on_post.delay(instance.pk, u.pk)  # рассылка писем

# # если произошло добавление новости, то подписанным пользователям отправляем письма
# @receiver(post_save, sender=Post)
# def send_mail_on_post(sender, instance, **kwargs):
#     cats = instance.categories.all() # берем все категории
#     for c in cats:  # цикл по всем категориям
#         users = c.subscribers.all()  # бежим по связям, пользователей, которые подписаны на категории новостей, собираем этих пользователей
#         for u in users:
#             task_mail_on_post.delay(instance.pk, u.pk)  # рассылка писем

# Больше трех статей в сутки создавать одному автору запрещено
# @receiver(pre_save, sender=Post)
# def day_news_limit(sender, instance, **kwargs):
#     #user1 = instance.author.Author_User
#     #author1 = Author.objects.get(Author_User=user1)
#     today = timezone.now()
#     day1 = today - timedelta(days=1)
#     count = Post.objects.filter(author=instance.author, date_create__gte=day1).count()
#     if count>=3:
#         text = 'Больше трех статей в сутки создавать одному автору запрещено!'
#         return render(request, 'news/post_limit.html', {'text': text})


# приветственное письмо пользователю при регистрации в приложении
@receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def user_signed_up_(request, user, **kwargs):
    # user signed up now send email
    # send email part - do your self
    #user = User.objects.get(pk=user_id)
    # сообщение при регистрации
    m='вы успешно зарегистрированы в приложении'
    html_content = render_to_string(
        'email/after_register.html',
        {
            'username': user.username,  # получение имени пользователя
            'message': m
        }
    )
    # формирование письма
    msg = EmailMultiAlternatives(
        subject='Успешная регистрация в приложении NewsPortal',  # тема письма
        #body=' Поздравляем вас с успешной регистрацией',  # тело
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],  # это то же, что и recipients_list
        # берем email пользователя
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем