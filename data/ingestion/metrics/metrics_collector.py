import argparse
from utils.postgres import *
from utils.aws import *
from utils.utils import *

def metrics_collector(username):
    # establish connection with PostgreSQL database
    conn = Postgres.create_connection()

    # set access keys for AWS
    keys, empty = Postgres.get_aws_access_keys(conn, username)
    if empty:
        print("No AWS credentials found for account.")
        return
    set_aws_access_keys(keys)

    # establish connection with cloudwatch and ec2      
    cloudwatch = Cloudwatch_Client()
    ec2 = EC2_Client()


    print("Collecting new metrics!")
    # get metrics data for each instance
    for instance, host in ec2.all_instances:
        metrics_data, data_exists = cloudwatch.get_metrics(instance, host)
        
        if data_exists:
            for timestamp in metrics_data:
                # generate values for each field
                metric_values = generate_metric_values(timestamp, metrics_data, instance)

                # insert into database one row at a time
                Postgres.insert_data(conn, metric_values, data="metrics")
        else:
            pass

    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)

    args = parser.parse_args()

    metrics_collector(args.username)