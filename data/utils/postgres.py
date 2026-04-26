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
    

    def insert_data(conn, data_values, data):
        cur = conn.cursor()

        if data == "metrics":
            # try inserting values into database
            try:
                cur.execute("INSERT INTO metrics (metricTime, instanceID, cpu, network, memory) VALUES (%s, %s, %s, %s, %s);", 
                            (data_values['metricTime'],data_values['instanceID'],data_values['cpu'],data_values['network'],data_values['memory']))                
                # commit changes
                conn.commit()     
             
            # catch errors when primary key is violated
            except errors.UniqueViolation:
                conn.rollback()
                print(f"Data exist in metrics table for instance {data_values['instanceID']} at {data_values['metricTime']}")
                
                cur.close()
                return False

        elif data == "logs":
            # try inserting values into database
            try:
                cur.execute("INSERT INTO logs (eventTime, errorCode, errorMessage, serviceName, eventName) VALUES (%s, %s, %s, %s, %s);", 
                            (data_values['eventTime'],data_values['errorCode'],data_values['errorMessage'],data_values['serviceName'],data_values['eventName']))                
                # commit changes
                conn.commit()            

            # catch errors when primary key is violated
            except errors.UniqueViolation:
                print(f"Data exist in logs table for error code - {data_values['errorCode']} and error message - {data_values['errorMessage']} at {data_values['eventTime']}")
                conn.rollback()

                cur.close()
                return False
        else:
            cur.close()
            return


        cur.close()
        return True
    