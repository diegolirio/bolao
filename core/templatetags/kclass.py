__author__ = 'toninhonunes'
from django import template
register = template.Library()

@register.filter('kclass')
def kclass(obj):
    return  'Ola ' + obj

def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')	
