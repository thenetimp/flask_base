from flask import Blueprint, request,  session, render_template, url_for, redirect
from flask_login import current_user

core_views = Blueprint('core_views', __name__)

##############################
# login user page
##############################
@core_views.route('/')
def page_index():
    return render_template('v1/core/index.html')
    
    
@core_views.route('/terms-of-service')
def page_terms_of_service():
    return render_template('v1/core/terms_of_service.html')    


@core_views.route('/welcome')
def page_welcome():
    return render_template('v1/core/welcome.html')    
