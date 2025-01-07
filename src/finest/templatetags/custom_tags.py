'''Custom Template Tag'''
from django import template

register = template.Library()

@register.filter
def range_filter(value):
    '''Custom Template Tag'''
    return range(value)
