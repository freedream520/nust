from django import template

register = template.Library()

@register.filter
def range(value):
    return xrange(value)

@register.filter
def divide(value, arg):
    return int(value) / int(arg)