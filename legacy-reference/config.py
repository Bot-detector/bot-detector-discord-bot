import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv(), verbose=True)

TOKEN = os.environ.get('TOKEN')
COMMAND_PREFIX = os.environ.get('COMMAND_PREFIX')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME_SUBMISSIONS = os.environ.get('DB_NAME_SUBMISSIONS')
DB_NAME_PLAYERS = os.environ.get('DB_NAME_PLAYERS')
API_AUTH_TOKEN = os.environ.get('API_AUTH_TOKEN')
SUBMIT_RECIPIENT = os.environ.get('SUBMIT_RECIPIENT')