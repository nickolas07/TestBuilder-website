from django import template

register = template.Library()


@register.filter
def index(value_list, value):
    return value_list[value] if value_list[value][0] is not None else None
