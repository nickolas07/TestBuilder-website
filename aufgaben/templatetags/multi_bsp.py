from django import template
import random

register = template.Library()


@register.filter
def multi_bsp(value):
    if value == 0:
        value = 1
    return ', '.join([str(random.randint(1, 10)) for _ in range(value)])
