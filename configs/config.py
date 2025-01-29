import base64
import logging
import os

from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)


OPEN_API_KEY = os.environ.get('OPEN_API_KEY')
DB_SCHEMA = os.environ.get('DB_SCHEMA')
DB_TABLE =  os.environ.get('DB_TABLE')
DATASTORE_TYPE = 'sqllite'