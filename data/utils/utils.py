# utility helper functions to abstract and moudlarize code
import re

# list of services to monitor for errors
MONITORED_SERVICES = ["EC2", "S3", "LAMBDA", "IAM", "STS", "RDS", "VPC", "ECS", "EKS", "SQS", "SNS", 
                       "API_GATEWAY", "CLOUDFORMATION", "CLOUDWATCH", "GUARDDUTY", "CONFIG", "ELB", 
                       "AUTOSCALING", "DYNAMODB", "KMS", "SECRETS_MANAGER", "GLUE", "LAKEFORMATION", 
                       "ATHENA", "REDSHIFT", "EMR", "KINESIS", "FIREHOSE", "STEP_FUNCTIONS", "EVENTBRIDGE", 
                       "CODEBUILD", "CODEPIPELINE", "CODEDEPLOY","CODEARTIFACT"]

def generate_metric_values(timestamp, metrics_data, instance):
    # database schema for table "metrics"
    metricTime = timestamp
    instanceID = instance
    cpu = round(metrics_data[timestamp]['cpu'],2)
    network = round(metrics_data[timestamp]['network_in'] + metrics_data[timestamp]['network_out'],2)
    memory = round(metrics_data[timestamp]['mem_used'],2)

    return {"metricTime": metricTime,
            "instanceID": instanceID,
            "cpu": cpu,
            "network": network, 
            "memory": memory }
    

def generate_error_values(error_events):
    # database schema for table "logs"
    eventTime = error_events["eventTime"]
    errorCode = error_events["errorCode"]
    errorMessage = error_events["errorMessage"]
    serviceName = extract_service(error_events["eventSource"])
    eventName = error_events["eventName"]

    return {"eventTime": eventTime,
            "errorCode": errorCode,
            "errorMessage": errorMessage,
            "serviceName": serviceName, 
            "eventName": eventName }, serviceName

# extract service from event source
def extract_service(eventSource):
    return re.findall(r'[a-z0-9]*\.',eventSource)[0].strip(".").upper()