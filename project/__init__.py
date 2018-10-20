# Import the base modules we'll be using.
import sys
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flaskext.sass import sass

# Create the flask applications
app = Flask(__name__)
sass(app, input_dir='assets/scss', output_dir='css')

try:
    app.config.from_envvar('FLASK_BASE_CONFIG')
except:
    print("\nEnvironment variable \"FLASK_BASE_CONFIG\" is not defined.")
    print("\"FLASK_BASE_CONFIG\" is the path to the program config file.\n\n")
    sys.exit()

# Instanciate the database
db = SQLAlchemy(app)
Migrate(app, db)

#################################
# Login Manager setup (after database instanciation)
#################################
login_manager = LoginManager();
login_manager.init_app(app)
login_manager.login_view='account.page_login'

#################################
# Miscellanious setup
#################################
bcrypt = Bcrypt()

# Import the blueprints after database instanciation    
from .views.core_views import core_views
from .views.user_views import user_views
from .utils.filters import filters

# Register the blueprints
app.register_blueprint(filters)
app.register_blueprint(core_views)
app.register_blueprint(user_views)