from django import template

register = template.Library()

bad_words = ['редиска', 'дурак']


@register.filter()
def censor(value):
    new_value = value

    if isinstance(value, str):
        for i in bad_words:
            new_value = new_value.replace(i[1:], '*'*(len(i) - 1))

    return new_value









