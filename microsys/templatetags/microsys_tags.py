from django import template
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

register = template.Library()

@register.simple_tag(takes_context=True)
def include_if_exists(context, template_name):
    """
    Include a template if it exists, otherwise do nothing.
    Usage: {% include_if_exists 'path/to/template.html' %}
    """
    try:
        t = get_template(template_name)
        return t.render(context.flatten())
    except TemplateDoesNotExist:
        return ""
