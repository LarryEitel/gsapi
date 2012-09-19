# -*- encoding:utf-8 -*-
from flask import Blueprint, request, render_template, session, jsonify, redirect, url_for
#from models.contact import Contact
import models
import mimerender
from bson.json_util import dumps
#from ex.models.users import User
#from ex.views import common
#from ex.views.generic import PaginatedListView
#from ex.views.utils import login_required

# from ex.extensions import db

contacts = Blueprint('contacts', __name__)

mimerender  = mimerender.FlaskMimeRender()

render_xml  = lambda message: '<message>%s</message>'%message
render_json = lambda **args: dumps(args)
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt  = lambda message: message

# index = PaginatedListView.as_view('contacts_list', template_name='contacts/list.html', model=Contact)

# index = render_template('/index.html')

# def detail(contact_id):
#     contacts = Contacts.query.get_or_404(contact_id)
#     return render_template('contacts/detail.html', contacts=contacts)



#contacts.add_url_rule('/find<regex:.*:q>', 'find', view_func=common.find)
# contacts.add_url_rule('/', 'index', view_func=index)
# contacts.add_url_rule('/<_id>/', 'detail', view_func=detail)
# @contacts.route( '/', methods=['GET'] )
@contacts.route( '/', methods=['GET', 'PUT'] )
@mimerender(
    default = 'html',
    html = render_html,
    xml = render_xml,
    json = render_json,
    txt = render_txt
)
def index():
    return {'message': 'Hello World!'}

