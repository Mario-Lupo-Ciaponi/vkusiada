from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_query_append(context, field, value):
    query_params = context["request"].GET.copy()
    query_params[field] = value

    return query_params.urlencode()
