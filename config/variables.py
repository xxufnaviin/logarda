
# list of services to monitor for errors
MONITORED_SERVICES = ["EC2", "S3", "LAMBDA", "IAM", "STS", "RDS", "VPC", "ECS", "EKS", "SQS", "SNS", 
                       "API_GATEWAY", "CLOUDFORMATION", "CLOUDWATCH", "GUARDDUTY", "CONFIG", "ELB", 
                       "AUTOSCALING", "DYNAMODB", "KMS", "SECRETS_MANAGER", "GLUE", "LAKEFORMATION", 
                       "ATHENA", "REDSHIFT", "EMR", "KINESIS", "FIREHOSE", "STEP_FUNCTIONS", "EVENTBRIDGE", 
                       "CODEBUILD", "CODEPIPELINE", "CODEDEPLOY","CODEARTIFACT"]

# PostgreSQL
METRICS_TABLE = 'metrics'
PREDICTED_METRICS_TABLE = "predicted_metrics"
LOGS_TABLE = "logs"

