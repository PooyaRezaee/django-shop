from django import template

register = template.Library()

@register.filter
def remove_page_param(query_params):
    params = query_params.copy()
    params.pop('page', None)
    return params.urlencode()


@register.filter
def remove_sorted_param(query_params):
    params = query_params.copy()
    params.pop('sorted_by', None)
    return params.urlencode()
