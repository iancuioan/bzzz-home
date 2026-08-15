from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    base_class = css_class
    if field.errors:
        base_class += ' is-invalid'
    return field.as_widget(attrs={**field.field.widget.attrs, "class": base_class})
