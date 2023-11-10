
from django.core.cache import cache
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import *
from .forms import *
import pytz
from django.utils.translation import gettext as _
from django.utils import timezone
from .models import Post, POST_TYPES, news as string_news, article as string_article
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

paginator_count = 10

class NewsList(ListView):
    model = Post
    ordering = '-date_create'
    categoryType = 'NS'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = paginator_count

class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'




class NewDetail(DetailView):
    model = Post
    template_name = 'Full_new.html'
    context_object_name = 'new'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class Search(ListView):
    model = Post
    ordering = '-date_create'
    categoryType = 'NS'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = paginator_count

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsCreate(LoginRequiredMixin, CreateView):
    permission_required = ('news_create',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.categoryType = string_news
        try:
            author1 = Author.objects.get(Author_User=self.request.user)
            news.author = author1
        except ObjectDoesNotExist:
            author1=Author()
            author1.Author_User=self.request.user
            author1.save()
            news.author = author1

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_title'] = ('Создание новости:')
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

class ArticleCreate(LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.categoryType = string_article
        try:
            author1 = Author.objects.get(Author_User=self.request.user)
            news.author = author1
        except ObjectDoesNotExist:
            author1 = Author()
            author1.Author_User = self.request.user
            author1.save()
            news.author = author1
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_title'] = ('Создание статьи:')
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

class PostEdit(LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_title'] = ('Редактирование новости:')
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


class PostDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = reverse_lazy('news_list')
    template_name = 'user_edit.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('news_list')

class UserDataUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserDataForm
    model = User
    template_name = 'user_edit.html'
    success_url = reverse_lazy('news_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Редактирование данных пользователя:')
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def get_object(self):
        return self.request.user


def logout_user(request):
    logout(request)
    return redirect('news_list')

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    Author.objects.create(Author_User=user)
    return redirect('news_list')

@login_required
def subscribe_on_cat(request, cat_id):
    user = request.user.id
    cat = Category(id=cat_id)
    cat.subscribers.add(user)
    return redirect('category')



@login_required
def unsubscribe_cat(request, cat_id):
    user = request.user.id
    cat = Category(id=cat_id)
    cat.subscribers.remove(user)
    return redirect('category')
