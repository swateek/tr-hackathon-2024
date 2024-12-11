"""__init__"""

from flask import Flask
from dotenv import load_dotenv


def create_app():
    """create_app"""
    load_dotenv()
    app = Flask(__name__)

    with app.app_context():
        # from . import routes

        return app
