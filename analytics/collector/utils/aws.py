import boto3


# only used as namespace for module, not OOP
class AWS:
    AWS_REGION = "ap-southeast-1"

    # establish connection with AWS services
    def create_client(service:str):
        return boto3.client(service, region_name=AWS.AWS_REGION)
    
    