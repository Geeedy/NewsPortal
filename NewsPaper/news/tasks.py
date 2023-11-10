from django.core.mail import EmailMultiAlternatives
from celery import shared_task
import time
from django.template.loader import render_to_string
from django.contrib.sites.models import Site  # Site.objects.get_current().domain
from django.conf import settings
from datetime import datetime, timedelta
import time
from .models import *


@shared_task
def task_mail_on_post(post_id, user_id):  # задача выслать электронное письмо в html формате при создании новости
    domain = Site.objects.get_current().domain
    # 'https://%s%s' % (Site.objects.get_current().domain, obj.get_absolute_url())
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=user_id)
    path = post.get_absolute_url()
    html_content = render_to_string(
        'email/new_post.html',
        {
            'username': user.username,  # получение имени пользователя
            'message': post.text[:50] + '...',  # 50 символов текста статьи
            'post_url': f'http://{domain}{path}',  # формирование url поста
        }
    )
    # формирование письма
    msg = EmailMultiAlternatives(
        subject=f'{post.title}',  # тема письма
        body=post.text[:50] + '...',  # тело
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],  # это то же, что и recipients_list
        # берем email пользователя
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем


@shared_task
def task_mail_week(post_id, user_id):  # задача выслать электронное письмо в html формате при создании новости
    # определить время неделю
    week_back = datetime.today() - timedelta(days=7)
    cats = Category.objects.all()  # берем все категории
    domain = Site.objects.get_current().domain  # для формирования ссылки
    # пройтись по всем категориям, подписанным пользователям сформировать и выслать все новости за неделю
    for c in cats:  # цикл по всем категориям
        users = c.subscribers.all()  # бежим по связям, пользователей, которые подписаны на категории новостей, собираем этих пользователей
        posts = Post.objects.filter(date_create__gte=week_back,
                                    categories=c)  # фильтрация постов неделя назад и по выбранной категории
        if posts.count() > 0:  # если были публикации
            for u1 in users:  # бежим по выбранным пользователям
                p = c.get_absolute_url()  # формирование ссылки
                html_content = render_to_string( # формирование тела письма в html формате
                    'email/post_week.html',
                    {
                        'username': u1.username,  # получение имени пользователя
                        'cat_name': c.name,
                        'cat_url': f'http://{domain}{p}',
                        'posts': posts,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f'Последние публикации-{c.name}',
                    body=f'Рассылка последних публикаций из категории "{c.name}".',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[u.email],  # это то же, что и recipients_list
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем