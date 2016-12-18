from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from app.models import NFL_Conference, League, Sport, SiteUser

#from nfl.viewmodels import SuperUser_Index,  SuperUser_Create, SuperUser_Edit, SuperUser_Details
#from nfl.viewmodels import User_Delete

#from nfl.forms import LeagueForm_Create, LeagueForm_Edit

class home(View):

    title = 'NFL - Home'
    template_name = 'nfl/home.html'

    def get(self, request, link_id = 0, modelstate = None ):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        link_id = int(link_id)

        viewmodel = {
                        'title':'NFL - Home',
                        'year':datetime.now().year,
                        'site_user': site_user,
                        'link_id' : link_id,   
                     }
        
        return render(request, self.template_name, viewmodel)

