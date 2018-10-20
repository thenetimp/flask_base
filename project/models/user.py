from flask import session
from flask_login import UserMixin, current_user, login_user, logout_user, current_user
from project.utils.encryption import encrypt_string, validate_string
from project import db, login_manager
from sqlalchemy import or_, desc
from datetime import datetime, timedelta
from project import bcrypt
import uuid


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(length=255), nullable=False)
    last_name = db.Column(db.String(length=255), nullable=False)
    display_name = db.Column(db.String(length=255), nullable=False, unique=True)
    email_address = db.Column(db.String(length=255), nullable=False, unique=True)
    email_address_normalized = db.Column(db.String(length=255))
    password_hash = db.Column(db.String(length=255), nullable=False)
    tos_agreed_at = db.Column(db.DateTime, nullable=False)
    password_request_token = db.Column(db.String(length=255), nullable=True)
    password_request_token_expire_at = db.Column(db.DateTime, nullable=True)
    validation_token = db.Column(db.String(length=255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, first_name, last_name, email_address,  password, display_name):
        now = datetime.now()
        
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.display_name = display_name
        self.tos_agreed_at = datetime.now()
        self.created_at = now
        self.modified_at = now
        self.validation_token = uuid.uuid4().hex

        self.encrypt_password(password)
        email_identifier_domain = self.email_address.split("@")
        email_identifier_filter = email_identifier_domain[0].split("+")
        self.email_address_normalized = "{}@{}".format(email_identifier_filter[0], email_identifier_domain[1])


    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


    def encrypt_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password=password)
        self.password_request_token = None
        self.password_request_token_expire_at = None


    def update_password_and_save(self, password):
        self.password_hash = bcrypt.generate_password_hash(password=password)
        self.password_request_token = None
        self.password_request_token_expire_at = None
        db.session.add(self)
        db.session.commit()


    def user_fullname(self):
        return "{} {}".format(self.first_name, self.last_name)
        

    @staticmethod
    def clear_password_token(email_address):
        user = User.query.filter_by(email_address=email_address).first()
        user.password_request_token = None
        user.password_request_token_expire_at = None
        db.session.add(user)
        db.session.commit()
        return user


    @staticmethod
    def create_user(first_name, last_name, email_address, password, display_name):
        user = User(first_name=first_name, last_name=last_name, email_address=email_address, password=password, display_name=display_name)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return user


    @staticmethod
    def generate_password_reset_token(email_address):
        
        # Get the user by email address
        user = User.query.filter_by(email_address=email_address).first()

        if user != None:
            if (user.password_request_token == None or user.password_request_token == "" or 
               (user != None and (user.password_request_token != "" or user.password_request_token != None) and 
               user.password_request_token_expire_at < datetime.now())):
                token = uuid.uuid4().hex
                user.password_request_token = token
                user.password_request_token_expire_at = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now() + timedelta(hours=24))
                db.session.add(user)
                db.session.commit()

        # Retuen the user object    
        return user


    @staticmethod
    def get_user_by_reset_token(reset_token):
        user = User.query.filter_by(password_request_token=reset_token).first()
        return user


    @staticmethod
    def login_user(email_address, password):
        user = User.query.filter_by(email_address=email_address).first()
        if user != None and user.check_password(password):
            login_user(user)
            return user
        return None


    @staticmethod
    def logout_user():
        logout_user()
        return None


    @staticmethod
    def save_password(email_address, password):
        user = User.query.filter_by(email_address=email_address).first()
        user.encrypt_password(password)
        db.session.add(user)
        db.session.commit()
        return user