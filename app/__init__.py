from flask import Flask
from app.api import bp as api_bp

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')

from app import routes
