from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse

news = 'NS'
article = 'AR'

POST_TYPES = [
    (news, 'Новость'),
    (article, 'Статья'),
    ]

world_events = 'WE'
politics = 'PO'
culture = 'CU'
economics = 'EC'
science = 'SC'
sport = 'SP'
another = 'AN'

CATEGORY_NEWS = [
    (world_events, 'мировые события'),
    (politics, 'политика'),
    (culture, 'культура'),
    (economics, 'экономика'),
    (science, 'наука'),
    (sport, 'спорт'),
    (another, 'другое'),

]



class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=80, choices=POST_TYPES, default=news)
    date_create = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=150)
    show_title = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:128]+'...'

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])




class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, choices=CATEGORY_NEWS, default=another, unique=True)
    subscribers = models.ManyToManyField(User, through='SubscribersCategory')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})


class PostCategory(models.Model):
    postLink = models.ForeignKey(Post, on_delete=models.CASCADE)
    CategoryLink = models.ForeignKey(Category, on_delete=models.CASCADE)


class SubscribersCategory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class Author(models.Model):
    Author_User = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        author_post_rating = Post.objects.filter(author_id=self.pk).aggregate(r1=Coalesce(Sum('rating'), 0))['r1']
        author_comments_rating = \
        Comment.objects.filter(commentUser_id=self.Author_User).aggregate(r2=Coalesce(Sum('rating'), 0))['r2']
        author_post_commits_rating = \
        Comment.objects.filter(commentUser_id=self.Author_User).aggregate(r3=Coalesce(Sum('rating'), 0))['r3']
        self.rating = author_post_rating * 3 + author_comments_rating + author_post_commits_rating
        self.save()

