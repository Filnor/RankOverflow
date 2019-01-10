import firebase_admin
from flask import Flask
from config import Config
from firebase_admin import credentials

app = Flask(__name__)

app.config.from_object(Config)

# Use the application default credentials
cred = credentials.Certificate("./service_account_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': Config().db_url,
})

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')
from app import routes
