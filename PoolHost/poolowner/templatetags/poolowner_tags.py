from django import template
    
register = template.Library()
register.simple_tag(lambda x: 3, name='filter_3')
register.simple_tag(lambda x: 2, name='filter_2')
register.simple_tag(lambda x: 1, name='filter_1')
register.simple_tag(lambda x: 0, name='filter_0')

register.simple_tag(lambda x: x, name='change_name')
register.simple_tag(lambda x: 0, name='groupowner_0')