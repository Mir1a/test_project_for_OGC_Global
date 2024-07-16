import os
from dotenv import load_dotenv

load_dotenv()

SECRET_AUTH = os.getenv("SECRET_AUTH")
if SECRET_AUTH is None:
    raise ValueError("SECRET_AUTH is not set in the environment variables")

DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
