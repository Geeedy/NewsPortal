import django_filters
from django.forms import DateInput
from django_filters import FilterSet, filters
from .models import *


class NewsFilter(FilterSet):
    row_date = django_filters.DateFilter(
        field_name='date_create',
        lookup_expr='gt',
        widget=DateInput(attrs={'type': 'date'}),
        label='Дата'
    )
    title = django_filters.CharFilter(lookup_expr='icontains', label='Заголовок')
    text = django_filters.CharFilter(lookup_expr='icontains', label='Текст публикации')
    categoryType = django_filters.CharFilter(lookup_expr='exact', label='Тип (NS - новость, AR - статья)')

    categories = django_filters.CharFilter(lookup_expr='icontains', label='Категория')


class Meta:
    model = Post
    fields = ['title', 'text', 'categoryType',
              'categories',
              ]