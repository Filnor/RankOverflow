from flask import Flask
from config import Config
#from app.models.__init__ import db
from flask_migrate import Migrate
from app.models.Score import Score
from app.models.CustomRank import CustomRank

app = Flask(__name__)
app.config.from_object(Config)

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

from app import routes
