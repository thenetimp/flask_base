from wtforms import ValidationError
from project.models import User


###############################################
# UniqueUserEmail Validator
###############################################
class UniqueUserEmail(object):
    def __init__(self, message=None):
        if message == None:
            self.message="This field must be unique"
        else:
            self.message=message

    def __call__(self, form, field):
        if User.query.filter_by(email_address=field.data).first():
            raise ValidationError(self.message)
            
###############################################
# UniqueUserEmail Validator
###############################################
class UniqueUserDisplayName(object):
    def __init__(self, message=None):
        if message == None:
            self.message="This field must be unique"
        else:
            self.message=message

    def __call__(self, form, field):
        if User.query.filter_by(display_name=field.data).first():
            raise ValidationError(self.message)
            
            