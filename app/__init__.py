from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app);
login_manager.login_view = 'index'

from . import views, models
