import boto3
from datetime import datetime, timezone, timedelta
import time
import json

class AWS_Client:
    
    def __init__(self, service):        
        self.AWS_REGION = "ap-southeast-1"    
        self.service = service

        # establish connection with AWS services
        self.client = boto3.client(self.service, region_name=self.AWS_REGION)

class EC2_Client(AWS_Client):

    def __init__(self):
        super().__init__("ec2")
        self.all_instances = self.get_instances()
    
    def get_instances(self):
        all_instances = []
        ec2_response = self.client.describe_instances()

        for reservation in ec2_response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                host_name = f"ip-{instance['PrivateIpAddress'].replace('.','-')}"
                all_instances.append((instance_id, host_name))

        return all_instances

class Cloudwatch_Client(AWS_Client):

    def __init__(self):
        super().__init__("cloudwatch")
        self.start_time = None
        self.end_time = None

    def get_metrics(self,instance_id, host_name):
        if self.service != "cloudwatch":
            print("Only AWS Cloudwatch Client can Get Metrics! Returning None.")
            return None, False

        self.end_time = datetime.now(timezone.utc)
        self.start_time = self.end_time - timedelta(minutes=20)

        # get cloudwatch metrics
        response = self.client.get_metric_data(
            MetricDataQueries=[
                {"Id": "cpu", "MetricStat": { "Metric": {
                                                        "Namespace": "AWS/EC2",
                                                        "MetricName": "CPUUtilization",
                                                        "Dimensions": [
                                                            {"Name": "InstanceId", "Value": instance_id}
                                                        ]
                        },"Period": 300, "Stat": "Average"
                        # the average over 5 minutes, as 5 minute interval is collected
                    }, "ReturnData": True},
                {"Id": "network_in", "MetricStat": { "Metric": {
                                                        "Namespace": "AWS/EC2",
                                                        "MetricName": "NetworkIn",
                                                        "Dimensions": [
                                                            {"Name": "InstanceId", "Value": instance_id}
                                                        ]
                        }, "Period": 300, "Stat": "Sum"
                    }, "ReturnData": True },

                {"Id": "network_out", "MetricStat": { "Metric": {
                                                        "Namespace": "AWS/EC2",
                                                        "MetricName": "NetworkOut",
                                                        "Dimensions": [
                                                            {"Name": "InstanceId", "Value": instance_id}
                                                        ]
                        }, "Period": 300, "Stat": "Sum"
                    }, "ReturnData": True },
                {"Id": "mem_used", "MetricStat": { "Metric": {
                                                        "Namespace": "CWAgent",
                                                        "MetricName": "mem_used_percent",
                                                        "Dimensions": [
                                                            {"Name": "host", "Value": host_name}
                                                        ]
                        }, "Period": 300, "Stat": "Average"
                    }, "ReturnData": True 
                }
            ],
            StartTime=self.start_time,
            EndTime=self.end_time
        )
        data = {}

        # loop through all metrics (cpu , network in, network out, memory)
        for result in response["MetricDataResults"]:
            # loop through each timestamp and values, insert into dictionary 
            # only if timestamp does not exist to ensure primary key constraint
            for timestamp, values in zip(result["Timestamps"], result["Values"]):
                if timestamp not in data:
                    data[timestamp] = {}
                data[timestamp][result["Id"]] = values

        return data, True
    
class Cloudtrail_Client(AWS_Client):

    def __init__(self):
        super().__init__("cloudtrail")
        self.all_events = []
        self.next_token = None
        self.target_event_count = 500
        self.error_events = []

    def get_error_events(self):
        self.get_all_events()
        self.filter_error_events()

        # only return data if exist
        if self.error_events:
            return self.error_events, True
        
        # else return None
        return None, False

    def get_all_events(self):
        # collect until length of events hit desired number
        while len(self.all_events) < self.target_event_count:
            # if subsequent pages of result (already have next token from first page), use next token
            if self.next_token:
                response = self.client.lookup_events(MaxResults=50, NextToken=self.next_token)
            # if first page of results, just get 50 rows
            else:
                response = self.client.lookup_events(MaxResults=50)
            
            events = response.get("Events", [])
            # extend list of all events since "events" is a list
            self.all_events.extend(events)

            # prevent getting rate limited by AWS API
            time.sleep(2)
            self.next_token = response.get("NextToken")
            if not self.next_token or len(events) == 0:
                break  # no more events available

    def filter_error_events(self):
        for i in self.all_events:
            cloudtrail_event = json.loads(i["CloudTrailEvent"])
            if "errorMessage" in cloudtrail_event:
                self.error_events.append(cloudtrail_event)

            