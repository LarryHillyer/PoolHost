class HelperMixins(object):

    @classmethod
    def get_all_items(cls, model_cls):
        return model_cls.objects.all()

    @classmethod
    def get_items_by_id(cls, model_cls, model_id):
        return model_cls.objects.filter(id = model_id)

    @classmethod
    def get_items_by_groupowner_id(cls, model_cls, model_groupowner_id):
        return model_cls.objects.filter(groupowner_id = model_groupowner_id)

    @classmethod
    def get_items_by_poolgroup_id(cls, model_cls, model_poolgroup_id):
        return model_cls.objects.filter(poolgroup_id = model_poolgroup_id)

    @classmethod
    def get_items_by_poolowner_id(cls, model_cls, model_poolowner_id):
        return model_cls.objects.filter(poolowner_id = model_poolowner_id)

    @classmethod
    def get_items_by_sport_id(cls, model_cls, model_sport_id):
        return model_cls.objects.filter(sport_id = model_sport_id)

    @classmethod
    def get_items_by_league_id(cls, model_cls, model_league_id):
        return model_cls.objects.filter(league_id = model_league_id)

    @classmethod
    def get_items_by_conference_id(cls, model_cls, model_conference_id):
        return model_cls.objects.filter(conference_id = model_conference_id)


    @classmethod
    def get_items_by_name(cls, model_cls, model_name):
        return model_cls.objects.filter(name = model_name)

    @classmethod
    def get_items_by_userid(cls, model_cls, model_userid):
        return model_cls.objects.filter(user_id = model_userid)

    @classmethod
    def get_items_without_dups(cls, model_cls, model_list_with_dups):
        items_without_dups = []
        item_names = []
        for item in model_list_with_dups:
            if not(item.name in item_names):
                items_without_dups.append(item)
                item_names.append(item.name)
        return items_without_dups


    @classmethod
    def get_item_by_id(cls, model_cls, model_id):
        model = None
        try:
            model = model_cls.objects.get(id = model_id)
        except:
            pass
        return model

    @classmethod
    def get_item_by_name(cls, model_cls, model_name):
        model = None
        try:
            model = model_cls.objects.get(name = model_name)
        except:
            pass
        return model

    @classmethod
    def get_item_by_userid(cls, model_cls, model_user_id):
        model = None
        try:
            model = model_cls.objects.get(user_id = model_user_id)
        except:
            pass
        return model

    @classmethod
    def add_item(cls, model_cls, model):
        try:
            model_cls.save(model)
            modelstate = 'Success: ' + model.name + ' has been added!'
        except:
            modelstate = 'Error: Database Error!!! ' + model.name + ' was not added!'
        return modelstate

    @classmethod
    def edit_item(cls, model_cls, model):
        try:
            model_cls.save(model)
            modelstate = 'Success: ' + model.name + ' has been edited!'
        except:
            modelstate = 'Error: Database Error!!! ' + model.name + ' was not edited!'
        return modelstate

    @classmethod
    def delete_item(cls, model_cls, model):
        try:
            model_cls.delete(model)
            modelstate = 'Success: ' + model.name + ' has been deleted!'
        except:
            modelstate = 'Error: Database Error!!! ' + model.name + ' was not deleted!'
        return modelstate
    
    @classmethod
    def get_modelstate(cls, modelstate):
        modelsuccess_bool = False
        if modelstate == None:  
            modelstate = ''
        else:
            try:
                modelstate.split(':')
                if modelstate.split(':')[0] == "Success":
                    modelsuccess_bool = True
                else:
                    modelsuccess_bool = False
            except:
                pass
        return modelstate, modelsuccess_bool
