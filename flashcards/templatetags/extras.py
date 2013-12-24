from django import template

register = template.Library()

#get the id of an object in a collection
@register.filter(name="id")
def get_id(d):
    try:
        d_id = d.get("_id")
        if not d_id is None:
            return str(d_id)
        else:
            return None
    except Exception:
        return None
