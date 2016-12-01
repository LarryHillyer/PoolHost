from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from app.models import CronJobType, SiteUser

from cronjobtype.viewmodels import SuperUser_Index, SuperUser_Create, SuperUser_Edit, SuperUser_Details, SuperUser_Delete
from cronjobtype.forms import CronJobTypeForm_Create, CronJobTypeForm_Edit

class index(View):

    template_name = 'app/shared_index.html'
    title = 'Pool Type - Index'
    
    def get(self, request, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')
        
        view_model = SuperUser_Index.get_index_viewmodel(site_user,self.title, modelstate)
        
        return render(request, self.template_name, view_model)
        
class create(View):

    template_name = 'app/shared_create.html'
    title = 'Cron Job Type - Create'

    def get(self, request, modelstate = None):
        
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        view_model = SuperUser_Create.get_create_viewmodel(site_user, self.title, modelstate)

        return render(request, self.template_name, view_model)
    
    def post(self, request, modelstate = None, **kwargs):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        cronjobtype = CronJobType(name = request.POST['name'])
        form = CronJobTypeForm_Create(request.POST)
        if form.is_valid():

            same_cronjobtype = CronJobType.objects.filter(name = cronjobtype.name)
            if same_cronjobtype.count() > 0:
                modelstate = 'Error: Pool type, ' + cronjobtype.name + ' is already a cronjobtype!'
                view_model = SuperUser_Create.get_create_viewmodel(site_user, form, modelstate)
                return render(request, self.template_name, view_model)
                                
            modelstate = CronJobType.add_item(CronJobType, cronjobtype)

            return HttpResponseRedirect(reverse('cronjobtype:index', args=(),
                                            kwargs = {'modelstate':modelstate}))
        else:
            view_model = SuperUser_Create.get_create_viewmodel(site_user, form, modelstate)
            return render(request, self.template_name, view_model)

class edit(View):
    title = 'Cron Job Type - Edit'
    template_name = 'app/shared_create.html'

    def get(self, request, cronjobtype_id = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if cronjobtype_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')
            
        cronjobtype_id = int(cronjobtype_id)

        viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, cronjobtype_id)

        return render(request, self.template_name, viewmodel)

    def post(self, request, cronjobtype_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        cronjobtype_id = int(cronjobtype_id)

        form = CronJobTypeForm_Edit(request.POST)

        if form.is_valid():

            exactly_same_cronjobtype = CronJobType.get_exactly_same_cronjobtype(form.data['id'], 
                form.data['name'])

            if exactly_same_cronjobtype.count() > 0:

                modelstate = 'Error: No Changes were made during edit, update aborted!'

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title,
                        modelstate, cronjobtype_id)

                return HttpResponseRedirect(reverse('cronjobtype:edit', args = (),
                                                        kwargs = {'modelstate': modelstate,
                                                                    'cronjobtype_id': cronjobtype_id}))
   
            same_cronjobtype = CronJobType.get_same_cronjobtype_in_database(form.data['name']) 

            if same_cronjobtype.count() > 0:
                modelstate = 'Error: Poolgroup is already in the database, update aborted!'    

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, 
                    cronjobtype_id)

                return HttpResponseRedirect(reverse('cronjobtype:edit', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'cronjobtype_id': cronjobtype_id}))

            cronjobtype = CronJobType.get_item_by_id(CronJobType, form.data['id'])
            cronjobtype.name = form.data['name']
            modelstate = CronJobType.edit_item(CronJobType, cronjobtype)

            if modelstate.split(':')[0] != 'Success':

                return HttpResponseRedirect(reverse('cronjobtype:edit', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'cronjobtype_id': cronjobtype_id}))

            return HttpResponseRedirect(reverse('cronjobtype:index', args = (),
                                                kwargs = {'modelstate': modelstate}))

        else:
            modelstate = 'Error: Invalid Input!'
 
            viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, 
                cronjobtype_id)

            return HttpResponseRedirect(reverse('cronjobtype:edit', args = (),
                                                kwargs = {'modelstate': modelstate,
                                                            'cronjobtype_id': cronjobtype_id}))

class details(View):

    title = 'Cron Job Type - Details'
    template_name = 'app/shared_details.html'

    def get(self, request, cronjobtype_id = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if cronjobtype_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        cronjobtype_id = int(cronjobtype_id)
        view_model = SuperUser_Details.get_details_viewmodel(site_user, self.title, 
            modelstate, cronjobtype_id )

        return render(request, self.template_name, view_model)

class delete(View):

    title = 'Cron Job Type - Delete'
    template_name = 'app/shared_delete.html'

    def get(self, request, cronjobtype_id = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if cronjobtype_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        cronjobtype_id = int(cronjobtype_id)

        view_model = SuperUser_Delete.get_delete_viewmodel(site_user, self.title, 
            modelstate, cronjobtype_id, )

        return render(request, self.template_name, view_model)

    def post(self, request, cronjobtype_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if cronjobtype_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        cronjobtype_id = int(cronjobtype_id)
        cronjobtype = CronJobType.get_item_by_id(CronJobType, cronjobtype_id)

        modelstate = CronJobType.delete_item(CronJobType, cronjobtype)

        return HttpResponseRedirect(reverse('cronjobtype:index', args=(),
                                    kwargs = {'modelstate':modelstate}))
