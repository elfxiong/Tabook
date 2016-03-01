from django import template

register = template.Library()


@register.simple_tag
def active_page(request, view_name_list):
    from django.core.urlresolvers import resolve, Resolver404
    if not request:
        return ""
    for view_name in view_name_list.split(','):
        try:
            if resolve(request.path_info).url_name == view_name:
                return "current"
        except Resolver404:
            pass
    return ""
