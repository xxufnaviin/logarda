import boto3
from datetime import datetime, timezone, timedelta
class AWS_Client:
    
    def __init__(self, service):        
        self.AWS_REGION = "ap-southeast-1"    
        self.service = service


        # establish connection with AWS services
        self.client = boto3.client(self.service, region_name=self.AWS_REGION)
        if self.service == "ec2":
            self.all_instances = self.get_instances()
        else:
            self.all_instances = None

        # for cloudwatch
        self.start_time = None
        self.end_time = None

        
    
    def get_instances(self):
        all_instances = []
        ec2_response = self.client.describe_instances()

        for reservation in ec2_response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                host_name = f"ip-{instance['PrivateIpAddress'].replace('.','-')}"
                all_instances.append((instance_id, host_name))

        return all_instances
    
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
