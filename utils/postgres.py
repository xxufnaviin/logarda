import psycopg2
from psycopg2 import errors
import config.secrets 
from config.variables import * 



# only used as namespace for module, not OOP
class Postgres:    
    def create_connection():
        return psycopg2.connect(host=config.secrets.POSTGRES_HOST, 
                            database=config.secrets.POSTGRES_DATABASE, 
                            user=config.secrets.POSTGRES_USER, 
                            password=config.secrets.POSTGRES_PASSWORD)
    

    def insert_data(conn, data_values, data):
        cur = conn.cursor()

        query_metrics = f"INSERT INTO {Postgres.metrics_table} (metricTime, instanceID, cpu, network, memory, username) VALUES (%s, %s, %s, %s, %s, %s);"
        query_logs = f"INSERT INTO {Postgres.logs_table} (eventTime, errorCode, errorMessage, serviceName, eventName, username) VALUES (%s, %s, %s, %s, %s, %s);"

        if data == "metrics":
            # try inserting values into database
            try:
                cur.execute(query_metrics,
                            (data_values['metricTime'],data_values['instanceID'],data_values['cpu'],data_values['network'],data_values['memory'], data_values['username']))                
                # commit changes
                conn.commit()     
             
            # catch errors when primary key is violated
            except errors.UniqueViolation:
                conn.rollback()
                print(f"Data exist in metrics table for instance {data_values['instanceID']} at {data_values['metricTime']}")
                
                cur.close()
                return False
            
            # catch errors when foreign key is violated
            except errors.ForeignKeyViolation:
                conn.rollback()
                print(f"Username does not exist in system {data_values['username']}")
                
                cur.close()
                return False

        elif data == "logs":
            # try inserting values into database
            try:
                cur.execute(query_logs, 
                            (data_values['eventTime'],data_values['errorCode'],data_values['errorMessage'],data_values['serviceName'],data_values['eventName'],data_values['username']))                
                # commit changes
                conn.commit()            

            # catch errors when primary key is violated
            except errors.UniqueViolation:
                print(f"Data exist in logs table for error code - {data_values['errorCode']} and error message - {data_values['errorMessage']} at {data_values['eventTime']}")
                conn.rollback()

                cur.close()
                return False
            
            # catch errors when foreign key is violated
            except errors.ForeignKeyViolation:
                conn.rollback()
                print(f"Username does not exist in system {data_values['username']}")
                
                cur.close()
                return False
        else:
            cur.close()
            return


        cur.close()
        return True
    
    def get_all_users(conn):
        cur = conn.cursor()
        query = f"SELECT username from {Postgres.user_table} WHERE collector_on = %s;"
        cur.execute(query, (True,))
        results = cur.fetchall()

        if results:
            cur.close()
            return [result[0] for result in results]
            
        
        cur.close()
        return None
    
    def get_aws_access_keys(conn, username):
        cur = conn.cursor()
        query = f"SELECT awskeyID, awskeySecret, awsRegion FROM {Postgres.user_table} WHERE username = %s;"
        cur.execute(query, (username,))
        result = cur.fetchone()

        if result and all(result):
            cur.close()
            return {
                "AWS_ACCESS_KEY_ID":result[0],
                "AWS_SECRET_ACCESS_KEY":result[1],
                "AWS_REGION":result[2]
            }, False
        
        cur.close()
        return None, True
    
    def set_env_tables():
        if config.secrets.ENVIRONMENT == "PRD":
            print("Production")
            Postgres.metrics_table = PRD_METRICS_TABLE
            Postgres.logs_table = PRD_LOGS_TABLE
            Postgres.user_table = PRD_USERS_TABLE
        else:
            print("Staging")
            Postgres.metrics_table = STG_METRICS_TABLE
            Postgres.logs_table = STG_LOGS_TABLE
            Postgres.user_table = STG_USERS_TABLE
        
    