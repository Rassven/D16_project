from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    temp = context['request'].GET.copy()
    for k_pos, k_value in kwargs.items():
        temp[k_pos] = k_value
    return temp.urlencode()
