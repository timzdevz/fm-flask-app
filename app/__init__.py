import os
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config

app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_CONFIG') or 'development'])

import logging
from logging import StreamHandler
file_handler = StreamHandler()
file_handler.setLevel(logging.ERROR)
app.logger.addHandler(file_handler)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app);
login_manager.login_view = 'index'
login_manager.login_message_category = "info"

from . import views, models
