from django import template
    
register = template.Library()

@register.inclusion_tag('poolgroup/create_link.html', takes_context = True)
def create_url(context):
    return {
        'create_link' : context['create_url'] + str(context['groupowner_id']) 
                        + '/' + str(context['filter']) + '/',
        'create_link_name' : context['create_link_name']
    }

@register.inclusion_tag('poolgroup/create_form.html', takes_context = True)
def create_form(context):
    return {
        'form_action' : context['form_url'] + str(context['groupowner_id']) 
                        + '/' + str(context['filter']) + '/',
        'form_html' : context['form_html'],
        'form_label_submit' : context['form_label_submit']

    }

