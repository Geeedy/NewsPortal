from django.urls import path
from .views import *


urlpatterns = [
   path('', NewsList.as_view()),
   path('news/<int:pk>/', NewDetail.as_view(), name='new_detail'),
   path('news/search/', Search.as_view(), name='search')
]