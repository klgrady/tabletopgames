import os
from os.path imporpt join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
PASSWORD = os.environ.get('PASSWORD')
SQLALCHEMY_TRACK_MODIFICATIONS = False