import argparse
from utils.postgres import *
from utils.aws import *
from utils.redis import *
from utils.utils import *
from config.variables import *

def logs_collector(username):
    # establish connection with PostgreSQL database and Redis 
    conn = Postgres.create_connection()
    r = Redis.create_connection()

    if config.secrets.ENVIRONMENT == "PRD":
        ERROR_QUEUE = "error_messages"
    else:
        ERROR_QUEUE = "stg_error_messages"

    # set access keys for AWS
    keys, empty = Postgres.get_aws_access_keys(conn, username)
    if empty:
        print("No AWS credentials found for account.")
        return
    set_aws_access_keys(keys)

    # establish connection with cloudtrail
    cloudtrail = Cloudtrail_Client()


    print("Checking for errors!")
    # insert error only logs into database
    error_events, data_exists = cloudtrail.get_error_events()

    if data_exists:
        for events in error_events:
            # generate values for each field
            error_values, service = generate_error_values(events, username)

            # insert into database one row at a time if error is relevant
            if service in MONITORED_SERVICES:                
                # check if value if succeed in inserting value into database, only enqueue redis if success
                if Postgres.insert_data(conn, error_values, data="logs"):
                    # enqueue errors into redis 
                    Redis.enqueue_message(r, ERROR_QUEUE, error_values)
                    
                else:
                    print("Duplicate errors will not be enqueued to Redis!")

            else:
                print(f"Errors in service - {service} are not monitored. Skipping the error event.")
                continue
            
    else:
        print("No error events for the past 15 minutes!")
        pass

    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)

    args = parser.parse_args()

    logs_collector(args.username)