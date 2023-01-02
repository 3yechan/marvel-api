import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    FLASK_APP = os.environ.get("FLASK_APP")