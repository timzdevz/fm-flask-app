from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

from . import views