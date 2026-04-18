from utils.postgres import *
from utils.aws import *

from datetime import datetime, timezone
import pandas as pd


# establish connection with cloudwatch and ec2      
cloudwatch = AWS.create_client("cloudwatch")
ec2_client = AWS.create_client("ec2")

# establish connection with PostgreSQL database
conn = postgres.create_connection()




if __name__ == "__main__":
    all_instances = []
    ec2_response = ec2_client.describe_instances()

    for reservation in ec2_response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            host_name = f"ip-{instance['PrivateIpAddress'].replace('.','-')}"
            all_instances.append((instance_id, host_name))

print(all_instances)
