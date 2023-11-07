from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
   path('', NewsList.as_view(), name='news_list'),
   path('news/<int:pk>/', NewDetail.as_view(), name='new_detail'),
   path('news/search/', Search.as_view(), name='search'),
   path('news/create/', NewsCreate.as_view(), name='new_create'),
   path('news/<int:pk>/edit/', PostEdit.as_view(), name='new_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='new_delete'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', PostEdit.as_view(), name='article_edit'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
   path('login/',
        LoginView.as_view(template_name='login.html'),
        name='login'),
   path('logout/',
        LogoutView.as_view(template_name='logout.html'),
        name='logout'),
   path('sign/signup/',
         BaseRegisterView.as_view(template_name='signup.html'),
         name='signup'),
]

