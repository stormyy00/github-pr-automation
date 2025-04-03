from flask import Flask
from app.routes import main  # ← important!

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app
