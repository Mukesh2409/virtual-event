from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_classes):
    """
    Add CSS classes to a form field
    Usage: {{ form.field|add_class:"custom-class" }}
    """
    return field.as_widget(attrs={"class": css_classes})