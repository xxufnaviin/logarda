from utils.postgres import *
from utils.aws import *
from utils.redis import *
from utils.utils import *
from config.variables import *
import config.secrets

# establish connection with PostgreSQL database and Redis
conn = Postgres.create_connection()
r = Redis.create_connection()

# set access keys for AWS
keys, empty = Postgres.get_aws_access_keys(conn, config.secrets.USERNAME)
if not empty:
    set_aws_access_keys(keys)

# establish connection with cloudtrail
cloudtrail = Cloudtrail_Client()

if __name__ == "__main__":
    print("Checking for errors!")
    # insert error only logs into database
    error_events, data_exists = cloudtrail.get_error_events()

    if data_exists:
        for events in error_events:
            # generate values for each field
            error_values, service = generate_error_values(events)

            # insert into database one row at a time if error is relevant
            if service in MONITORED_SERVICES:                
                # check if value if succeed in inserting value into database, only enqueue redis if success
                if Postgres.insert_data(conn, error_values, data="logs"):
                    # enqueue errors into redis 
                    Redis.enqueue_message(r, "error_messages", error_values)
                    
                else:
                    print("Duplicate errors will not be enqueued to Redis!")

            else:
                print(f"Errors in service - {service} are not monitored. Skipping the error event.")
                continue
            
    else:
        print("No error events for the past 15 minutes!")
        pass
    
    conn.close()