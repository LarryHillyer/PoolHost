from datetime import datetime

from django.db import models

from app.models import SiteUser, PoolOwner, PoolGroup, GroupOwner, SuperUser 
from app.models import GroupOwner_Choices, PoolGroup_Choices
from app.mixins import HelperMixins

from poolowner.forms import PoolOwnerForm_SuperUser_Create, PoolOwnerForm_SuperUser_Edit
from poolowner.forms import PoolOwnerForm_GroupOwner_Create, PoolOwnerForm_GroupOwner_Edit
