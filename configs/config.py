import base64
import logging
import os
import json

from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)


OPEN_API_KEY = os.environ.get('OPEN_API_KEY') if os.environ.get('OPEN_API_KEY') else None
DB_SCHEMA = os.environ.get('DB_SCHEMA') if os.environ.get('DB_SCHEMA') else None
DB_TABLE =  os.environ.get('DB_TABLE') if os.environ.get('DB_TABLE') else None
DATASTORE_TYPE = 'sqllite'