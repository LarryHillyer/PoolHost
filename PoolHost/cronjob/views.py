from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from app.models import CronJob, SiteUser

from cronjob.viewmodels import SuperUser_Index, SuperUser_Create, SuperUser_Edit, SuperUser_Details, SuperUser_Delete
from cronjob.forms import CronJobForm_Create, CronJobForm_Edit

class index(View):

    template_name = 'app/shared_index.html'
    title = 'Cron Job - Index'
    
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
    title = 'Cron Job - Create'

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

        cronjob = CronJob(name = request.POST['name'], cronjobtype_id = request.POST['cronjobtype_id'])
        form = CronJobForm_Create(request.POST)
        if form.is_valid():

            same_cronjob = CronJob.objects.filter(name = cronjob.name)
            if same_cronjob.count() > 0:
                modelstate = 'Error: Cron Job, ' + cronjob.name + ' is already a cronjob!'
                view_model = SuperUser_Create.get_create_viewmodel(site_user, form, modelstate)
                return render(request, self.template_name, view_model)
                                
            modelstate = CronJob.add_item(CronJob, cronjob)

            return HttpResponseRedirect(reverse('cronjob:index', args=(),
                                            kwargs = {'modelstate':modelstate}))
        else:
            view_model = SuperUser_Create.get_create_viewmodel(site_user, form, modelstate)
            return render(request, self.template_name, view_model)

class edit(View):
    title = 'Cron Job - Edit'
    template_name = 'app/shared_create.html'

    def get(self, request, cronjob_id = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if cronjob_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')
            
        cronjob_id = int(cronjob_id)

        viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, cronjob_id)

        return render(request, self.template_name, viewmodel)

    def post(self, request, cronjob_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        cronjob_id = int(cronjob_id)

        form = CronJobForm_Edit(request.POST)

        if form.is_valid():

            exactly_same_cronjob = CronJob.get_exactly_same_cronjob(form.data['id'], 
                form.data['name'], form.data['cronjobtype_id'])

            if exactly_same_cronjob.count() > 0:

                modelstate = 'Error: No Changes were made during edit, update aborted!'

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title,
                        modelstate, cronjob_id)

                return HttpResponseRedirect(reverse('cronjob:edit', args = (),
                                                        kwargs = {'modelstate': modelstate,
                                                                    'cronjob_id': cronjob_id}))
   
            same_cronjob = CronJob.get_same_cronjob_in_database(form.data['name']) 

            if same_cronjob.count() > 0:
                modelstate = 'Error: Poolgroup is already in the database, update aborted!'    

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, 
                    cronjob_id)

                return HttpResponseRedirect(reverse('cronjob:edit', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'cronjob_id': cronjob_id}))

            cronjob = CronJob.get_item_by_id(CronJob, form.data['id'])
            cronjob.name = form.data['name']
            cronjob.cronjobtype_id = form.data['cronjobtype_id']
            modelstate = CronJob.edit_item(CronJob, cronjob)

            if modelstate.split(':')[0] != 'Success':

                return HttpResponseRedirect(reverse('cronjob:edit', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'cronjob_id': cronjob_id}))

            return HttpResponseRedirect(reverse('cronjob:index', args = (),
                                                kwargs = {'modelstate': modelstate}))

        else:
            modelstate = 'Error: Invalid Input!'
 
            viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, 
                cronjob_id)

            return HttpResponseRedirect(reverse('cronjob:edit', args = (),
                                                kwargs = {'modelstate': modelstate,
                                                            'cronjob_id': cronjob_id}))

class details(View):

    title = 'Cron Job - Details'
    template_name = 'app/shared_details.html'

    def get(self, request, cronjob_id = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if cronjob_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        cronjob_id = int(cronjob_id)
        view_model = SuperUser_Details.get_details_viewmodel(site_user, self.title, 
            modelstate, cronjob_id )

        return render(request, self.template_name, view_model)

class delete(View):

    title = 'Cron Job - Delete'
    template_name = 'app/shared_delete.html'

    def get(self, request, cronjob_id = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if cronjob_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        cronjob_id = int(cronjob_id)

        view_model = SuperUser_Delete.get_delete_viewmodel(site_user, self.title, 
            modelstate, cronjob_id, )

        return render(request, self.template_name, view_model)

    def post(self, request, cronjob_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if cronjob_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        cronjob_id = int(cronjob_id)
        cronjob = CronJob.get_item_by_id(CronJob, cronjob_id)

        modelstate = CronJob.delete_item(CronJob, cronjob)

        return HttpResponseRedirect(reverse('cronjob:index', args=(),
                                    kwargs = {'modelstate':modelstate}))
