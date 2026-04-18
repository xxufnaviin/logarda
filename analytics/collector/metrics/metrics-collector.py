import postgres
import boto3
from datetime import datetime, timezone
import pandas as pd

AWS_REGION = "ap-southeast-1"
      
# establish connection with cloudwatch and ec2      
cloudwatch = boto3.client("cloudwatch", region_name=AWS_REGION)
ec2_client = boto3.client('ec2', region_name=AWS_REGION)

# establish connection with PostgreSQL database
# conn = 



if __name__ == "__main__":
    all_instances = []
    ec2_response = ec2_client.describe_instances()

    for reservation in ec2_response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            host_name = f"ip-{instance['PrivateIpAddress'].replace('.','-')}"
            all_instances.append((instance_id, host_name))


