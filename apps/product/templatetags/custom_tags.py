from django import template
from ..models import Category

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


@register.inclusion_tag('partials/category_tree.html')
def render_category_tree():
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('childs')
    return {'categories': categories}