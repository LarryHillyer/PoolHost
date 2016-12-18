"""
Definition of views.
"""
from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View

from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.models import User

from registration import signals
from app.forms import RegistrationForm
from app.models import SiteUser


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    site_user = None
    if request.user.is_authenticated():
        site_user = SiteUser.objects.filter(user_id = request.user.id)[0]

    template_name = 'app/home.html'

    view_model = {
                    'title':'Pool Host - Home',
                    'year':datetime.now().year,
                    'site_user': site_user,
                    'home_url': 'home'   
                 }

    return render(request, template_name, view_model)

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

class register(View):
    """Render the registration form"""
    form_class = RegistrationForm
    initial = {}
    template_name = 'app/registration.html'
    title = 'Register'

    def get(self, request):
        form = self.form_class(initial = self.initial)
        return render(request, self.template_name, { 'form': form, 'title': self.title })

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=getattr(new_user, User.USERNAME_FIELD),
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            signals.user_registered.send(sender=register.__class__,
                                         user=new_user,
                                         request=request)
            SiteUser(name = new_user.username, user_id = new_user.id).save()
            return HttpResponseRedirect('../../')
        else:
            return render(request, self.template_name, { 'form': form, 'title': self.title })
