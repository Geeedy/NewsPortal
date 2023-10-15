from django.views.generic import ListView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = '-date_create'
    categoryType = 'NS'
    template_name = 'news.html'
    context_object_name = 'news'
