from django import forms
from .models import *



class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)


    class Meta:
       model = Post
       fields = [
           'title',
           'categories',
           'text'
       ]
       labels = {
           'title': 'Заголовок',
           'categories': 'Категория',
           'text': 'текст публикации',
       }