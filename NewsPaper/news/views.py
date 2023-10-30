from django.views.generic import ListView, DetailView
from .models import Post
from django.core.cache import cache
from .filters import NewsFilter

paginator_count = 2

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