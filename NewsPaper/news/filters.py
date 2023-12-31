import django_filters
from django.forms import DateInput
from django_filters import FilterSet


class NewsFilter(FilterSet):

    title = django_filters.CharFilter(lookup_expr='icontains', label='Заголовок')
    author__Author_User__username = django_filters.AllValuesFilter(lookup_expr='exact', label='Автор')
    categories__name = django_filters.AllValuesFilter(lookup_expr='exact', label='Категория')

    row_date = django_filters.DateFilter(
        field_name='date_create',
        lookup_expr='gt',
        widget=DateInput(attrs={'type': 'date'}),
        label='Дата'
    )


