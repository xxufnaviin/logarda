import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")

# only used as namespace for module, not OOP
class postgres:
    def create_connection():
        return psycopg2.connect(host=POSTGRES_HOST, 
                            database=POSTGRES_DATABASE, 
                            user=POSTGRES_USER, 
                            password=POSTGRES_PASSWORD)