import psycopg2
from psycopg2 import errors
import config.secrets 


# only used as namespace for module, not OOP
class Postgres:
    def create_connection():
        return psycopg2.connect(host=config.secrets.POSTGRES_HOST, 
                            database=config.secrets.POSTGRES_DATABASE, 
                            user=config.secrets.POSTGRES_USER, 
                            password=config.secrets.POSTGRES_PASSWORD)
    

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
    
    def get_all_users(conn):
        cur = conn.cursor()
        cur.execute("SELECT username from users WHERE collector_on = %s;", (True,))
        results = cur.fetchall()

        if results:
            cur.close()
            return [result[0] for result in results]
            
        
        cur.close()
        return None
    
    def get_aws_access_keys(conn, username):
        cur = conn.cursor()
        cur.execute("SELECT awskeyID, awskeySecret, awsRegion FROM users WHERE username = %s;", (username,))
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
        
    