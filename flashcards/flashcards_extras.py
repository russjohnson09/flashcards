from django import template

register = template.Library()

#get the id of an object in a collection
@register.filter(name='id')
def get(d):
    return d.get("_id",None)
