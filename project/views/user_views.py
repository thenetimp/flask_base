from datetime import datetime, timedelta

from flask import Blueprint, request,  session, render_template, url_for, redirect, flash
from flask_login import current_user

from project.forms.user_forms import LoginForm, SignUpForm, ForgotPasswordForm, ForgotPasswordResetForm
from project.models import User
from project.utils.emails import send_password_reset_token
from project.uri_paths import uri_paths

user_views = Blueprint('user_views', __name__)

##############################
# User register
##############################
@user_views.route(uri_paths['user_signup'], methods=['GET','POST'])
def page_register():

    form = SignUpForm()

    if form.validate_on_submit():
        user = User.create_user(form.first_name.data, form.last_name.data, form.email_address.data,
                                form.password.data, form.display_name.data);
        return redirect(url_for('core_views.page_welcome'))

    return render_template('v1/user/sign-up.html', form=form)
    

##############################
# User Login
##############################
@user_views.route(uri_paths['user_login'], methods=['GET','POST'])
def page_login():
    
    form = LoginForm()
    if form.validate_on_submit():
        authentication = User.login_user(form.email_address.data, form.password.data)
        if authentication != None:
            return redirect(url_for('core_views.page_welcome'))
        else:
            flash("Invalid email address or password.  Please try again.", 'danger')
    
    return render_template('v1/user/log-in.html', form=form)
    

##############################
# User Login
##############################
@user_views.route(uri_paths['user_logout'], methods=['GET'])
def page_logout():
    User.logout_user()
    return redirect(url_for('core_views.page_index'))
    

##############################
# User Profile
##############################
@user_views.route(uri_paths['user_profile'], methods=['GET'])
def page_profile():
    return render_template('v1/user/profile.html')
    

##############################
# User Password Forget
##############################
@user_views.route(uri_paths['user_forgot_password'], methods=['GET','POST'])
def page_forgot_password():

    user = None
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.generate_password_reset_token(form.email_address.data)
        
        if user != None:
            send_password_reset_token(user.email_address, user.password_request_token)
            return redirect(url_for('user_views.page_forgot_password_request_processed'))
        else:
            flash('We can not find a user with that email address please try again.', 'danger')
    
    return render_template('v1/user/forgot-password.html', form=form, user=user)
    

##############################
# User Password Forget Processed
##############################
@user_views.route(uri_paths['user_forgot_password_processed'], methods=['GET','POST'])
def page_forgot_password_request_processed():
    return render_template('v1/user/forgot-password-processed.html')
    

##############################
# User Password Reset with Token
##############################
@user_views.route(uri_paths['user_password_reset_with_token'], methods=['GET','POST'])
def page_password_reset_with_token(reset_token):
    user = User.get_user_by_reset_token(reset_token);
    if user is None or user.password_request_token_expire_at is None:
        return render_template('v1/user/forgot-password-reset-token-invalid.html')
    elif user.password_request_token_expire_at < datetime.now():
        return render_template('v1/user/forgot-password-reset-token-expired.html')

    form = ForgotPasswordResetForm()
    
    if form.validate_on_submit():
        user.update_password_and_save(form.password.data)

        flash('Your password has been reset, please log in.', 'info')
        return redirect(url_for('user_views.page_login'))
    
    return render_template('v1/user/forgot-password-reset.html', form=form)
    

##############################
# User email address check
##############################
@user_views.route('/api/common/unique-email/<email_address>', methods=['POST'])
def page_api_unique_email(email_address):
    return False


##############################
# User display name check
##############################
@user_views.route('/api/common/unique-display-name/<display_name>', methods=['POST'])
def page_api_unique_display_name(display_name):
    return False

