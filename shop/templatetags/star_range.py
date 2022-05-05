from django import template

register = template.Library()

@register.filter
def starrange(value):
    return range(value)

@register.filter
def emptystarnumber(value):
    return 5 - value