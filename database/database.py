from pymongo import MongoClient
import os
from dotenv import load_dotenv

#  load environment variables from .env file
load_dotenv()

# get environment variables
MONGODB_URI= os.environ.get('MONGODB_URL')
print(MONGODB_URI)
DB_NAME = os.environ.get('DATABASE_NAME')
User = os.environ.get('COLLECTION_NAME_User')





client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
user = db.User

