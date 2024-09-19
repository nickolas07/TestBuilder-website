from django import template

register = template.Library()


@register.filter
def clean_auswahl(value):
    value = value.replace('_', ' ')

    temp = []
    for word in value.split(' '):
        if word.isupper():
            temp.append(word)
        else:
            temp.append(word.capitalize())

    return ' '.join(temp)
