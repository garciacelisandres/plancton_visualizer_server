from resources.create import create_app
from os import environ

from dotenv import load_dotenv
load_dotenv()

app = create_app(environ.get('ENVIRONMENT'))
