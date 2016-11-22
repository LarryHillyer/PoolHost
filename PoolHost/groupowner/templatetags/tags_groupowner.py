from django import template
    
register = template.Library()
register.simple_tag(lambda x: x, name='change_name')
