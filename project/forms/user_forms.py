from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField, PasswordField, SelectField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo 
from project.forms.validators import ProfileUniqueUserEmail, ProfileUniqueUserDisplayName, UniqueUserEmail, UniqueUserDisplayName


__ALL__ = [
 'ForgotPassword',   
 'LoginForm',
 'SignUp'
]


class ForgotPasswordForm(FlaskForm):
    email_address = EmailField('Email Address',validators=[DataRequired(), Email()])
    submit = SubmitField('Log In')


class ForgotPasswordResetForm(FlaskForm):
    email_address = EmailField('Email Address',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])    
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message="Passwords do not match")])    
    submit = SubmitField('Log In')


class LoginForm(FlaskForm):
    email_address = EmailField('Email Address',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])    
    remember = BooleanField('Remember me')    
    submit = SubmitField('Log In')


class ProfileEditForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    display_name = StringField('Display Name',validators=[DataRequired(), ProfileUniqueUserDisplayName("This display name is in use by another account.")])
    email_address = EmailField('Email Address',validators=[DataRequired(), Email(), ProfileUniqueUserEmail("This email address is in use by another account.")])
    submit = SubmitField('Save Profile')


class SignUpForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    display_name = StringField('Display Name',validators=[DataRequired(), UniqueUserDisplayName("This display name is in use by another account.")])
    email_address = EmailField('Email Address',validators=[DataRequired(), Email(), UniqueUserEmail("This email address is in use by another account.")])
    password = PasswordField('Password',validators=[DataRequired()])    
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message="Passwords do not match")])    
    submit = SubmitField('Register')
    
