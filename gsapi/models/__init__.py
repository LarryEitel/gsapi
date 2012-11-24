# from . import generic, contact
from mod import *
from generic import *
from tag import *
from embed import *
from rdt import *
from cnt import *
from pl import *
from wdg import *
# this allows the model parameter to map to the corresponding collection Model which is required for a few of these functions
# model_classes_by_route = {'contacts': contact.Contact, 'companys': contact.Company, 'persons': contact.Person, 'users':contact.User, 'emails':generic.Email}

# # gonna map model _cls to model class instances
# model_classes_by_id = {'cnt': contact.Contact, 'cmp': contact.Company, 'prs': contact.Person, 'usr':contact.User, 'eml':generic.Email}

