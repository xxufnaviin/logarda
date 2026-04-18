import psycopg2
from psycopg2 import errors
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")

METRICS_TABLE = 'metrics'
PREDICTED_METRICS_TABLE = "predicted_metrics"
LOGS_TABLE = "logs"

# only used as namespace for module, not OOP
class Postgres:
    def create_connection():
        return psycopg2.connect(host=POSTGRES_HOST, 
                            database=POSTGRES_DATABASE, 
                            user=POSTGRES_USER, 
                            password=POSTGRES_PASSWORD)
    

    def insert_metrics(conn, metric_values):
        cur = conn.cursor()
        # try inserting values into database
        try:
            cur.execute("INSERT INTO metrics (metricTime, instanceID, cpu, network, memory) VALUES (%s, %s, %s, %s, %s);", 
                        (metric_values[0],metric_values[1],metric_values[2],metric_values[3],metric_values[4]))
            
            # commit changes
            conn.commit()
        
        # catch errors when primary key is violated
        except errors.UniqueViolation:
            conn.rollback()
            print(f"Data exist in metrics table for instance {metric_values[1]} at {metric_values[0]}")

        cur.close()
    