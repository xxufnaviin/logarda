
# list of services to monitor for errors
MONITORED_SERVICES = ["EC2", "S3", "LAMBDA", "IAM", "STS", "RDS", "VPC", "ECS", "EKS", "SQS", "SNS", 
                       "API_GATEWAY", "CLOUDFORMATION", "CLOUDWATCH", "GUARDDUTY", "CONFIG", "ELB", 
                       "AUTOSCALING", "DYNAMODB", "KMS", "SECRETS_MANAGER", "GLUE", "LAKEFORMATION", 
                       "ATHENA", "REDSHIFT", "EMR", "KINESIS", "FIREHOSE", "STEP_FUNCTIONS", "EVENTBRIDGE"]

# PostgreSQL
PRD_METRICS_TABLE = 'metrics'
PRD_PREDICTED_METRICS_TABLE = "predicted_metrics"
PRD_LOGS_TABLE = "logs"
PRD_USERS_TABLE = 'users'

STG_METRICS_TABLE = 'stg_metrics'
STG_LOGS_TABLE = "stg_logs"
STG_USERS_TABLE = 'stg_users'





