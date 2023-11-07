from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.cache import cache
from .filters import NewsFilter
from .forms import PostForm
from .models import Post, Author, POST_TYPES, news as string_news, article as string_article
import pytz
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm

paginator_count = 10

class NewsList(ListView):
    model = Post
    ordering = '-date_create'
    categoryType = 'NS'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = paginator_count

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
    success_url = '/'
