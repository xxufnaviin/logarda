
import os
from dotenv import load_dotenv

load_dotenv()

# Postgres 
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
DATABASE = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DATABASE}"

# Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

# AWS (get dynamiccaly)
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None
AWS_REGION = None

USERNAME = os.getenv("USERNAME")
ENCRYPTION_KEY = bytes(os.getenv("ENCRYPTION_KEY"), 'utf-8')

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

ENVIRONMENT = os.getenv("ENVIRONMENT")
if not ENVIRONMENT:
    ENVIRONMENT = 'STG' # defaults to staging, if not overwritten by production


    