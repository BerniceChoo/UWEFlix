from django import template

register = template.Library()

@register.filter
def get_id(document):
    return str(document['_id'])
