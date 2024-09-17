from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    # Check if the value is a form field (BoundField)
    if isinstance(value, BoundField):
        return value.as_widget(attrs={"class": css_class})
    return value  # If it's not a form field, just return the value
