from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse

from app.models import PoolType, SiteUser

from pooltype.viewmodels import SuperUser_Index, SuperUser_Create, SuperUser_Edit, SuperUser_Details, SuperUser_Delete
from pooltype.forms import PoolTypeForm_Create, PoolTypeForm_Edit

class index(View):

    template_name = 'app/shared_index_view.html'
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

    template_name = 'app/shared_form_view.html'
    title = 'Pool Type - Create'

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

        pooltype = PoolType(name = request.POST['name'])
        form = PoolTypeForm_Create(request.POST)
        if form.is_valid():

            same_pooltype = PoolType.objects.filter(name = pooltype.name)
            if same_pooltype.count() > 0:
                modelstate = 'Error: Pool type, ' + pooltype.name + ' is already a pooltype!'
                view_model = SuperUser_Create.get_create_viewmodel(site_user, form, modelstate)
                return render(request, self.template_name, view_model)
                                
            modelstate = PoolType.add_item(PoolType, pooltype)

            return HttpResponseRedirect(reverse('pooltype:index', args=(),
                                            kwargs = {'modelstate':modelstate}))
        else:
            view_model = SuperUser_Create.get_create_viewmodel(site_user, form, modelstate)
            return render(request, self.template_name, view_model)

class edit(View):
    title = 'Pool Type - Edit'
    template_name = 'app/shared_form_view.html'

    def get(self, request, pooltype_id = 0, modelstate = None):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if pooltype_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')
            
        pooltype_id = int(pooltype_id)

        viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, pooltype_id)

        return render(request, self.template_name, viewmodel)

    def post(self, request, pooltype_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True and site_user.is_groupowner != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        pooltype_id = int(pooltype_id)

        form = PoolTypeForm_Edit(request.POST)

        if form.is_valid():

            exactly_same_pooltype = PoolType.get_exactly_same_pooltype(form.data['id'], 
                form.data['name'])

            if exactly_same_pooltype.count() > 0:

                modelstate = 'Error: No Changes were made during edit, update aborted!'

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title,
                        modelstate, pooltype_id)

                return HttpResponseRedirect(reverse('pooltype:edit', args = (),
                                                        kwargs = {'modelstate': modelstate,
                                                                    'pooltype_id': pooltype_id}))
   
            same_pooltype = PoolType.get_same_pooltype_in_database(form.data['name']) 

            if same_pooltype.count() > 0:
                modelstate = 'Error: Poolgroup is already in the database, update aborted!'    

                viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, 
                    pooltype_id)

                return HttpResponseRedirect(reverse('pooltype:edit', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'pooltype_id': pooltype_id}))

            pooltype = PoolType.get_item_by_id(PoolType, form.data['id'])
            pooltype.name = form.data['name']
            modelstate = PoolType.edit_item(PoolType, pooltype)

            if modelstate.split(':')[0] != 'Success':

                return HttpResponseRedirect(reverse('pooltype:edit', args = (),
                                                    kwargs = {'modelstate': modelstate,
                                                                'pooltype_id': pooltype_id}))

            return HttpResponseRedirect(reverse('pooltype:index', args = (),
                                                kwargs = {'modelstate': modelstate}))

        else:
            modelstate = 'Error: Invalid Input!'
 
            viewmodel = SuperUser_Edit.get_edit_viewmodel(site_user, self.title, modelstate, 
                pooltype_id)

            return HttpResponseRedirect(reverse('pooltype:edit', args = (),
                                                kwargs = {'modelstate': modelstate,
                                                            'pooltype_id': pooltype_id}))

class details(View):

    title = 'Pool Type - Details'
    template_name = 'app/shared_details_view.html'

    def get(self, request, pooltype_id = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if pooltype_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        pooltype_id = int(pooltype_id)
        view_model = SuperUser_Details.get_details_viewmodel(site_user, self.title, 
            modelstate, pooltype_id )

        return render(request, self.template_name, view_model)

class delete(View):

    title = 'Pool Type - Delete'
    template_name = 'app/shared_delete_view.html'

    def get(self, request, pooltype_id = 0, modelstate = None):
        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if pooltype_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        pooltype_id = int(pooltype_id)

        view_model = SuperUser_Delete.get_delete_viewmodel(site_user, self.title, 
            modelstate, pooltype_id, )

        return render(request, self.template_name, view_model)

    def post(self, request, pooltype_id = 0):

        site_user = None
        if request.user.is_authenticated():
            site_user = SiteUser.get_items_by_userid(SiteUser, request.user.id)[0]
        else:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if site_user.is_superuser != True:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        if pooltype_id == 0:
            return HttpResponseForbidden('<h1> Bad Request </h1>')

        pooltype_id = int(pooltype_id)
        pooltype = PoolType.get_item_by_id(PoolType, pooltype_id)

        modelstate = PoolType.delete_item(PoolType, pooltype)

        return HttpResponseRedirect(reverse('pooltype:index', args=(),
                                    kwargs = {'modelstate':modelstate}))
