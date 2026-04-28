# utility helper functions to abstract and moudlarize code
import re
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import config.secrets

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


def decrypt(ciphertext_b64: str, key: bytes) -> str:
    data = base64.b64decode(ciphertext_b64)

    # Go format: nonce + ciphertext + tag (all together)
    nonce_size = 12  # GCM standard nonce size in Go

    nonce = data[:nonce_size]
    ciphertext = data[nonce_size:]

    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    return plaintext.decode()


def set_aws_access_keys(keys):
    config.secrets.AWS_ACCESS_KEY_ID = decrypt(keys["AWS_ACCESS_KEY_ID"], config.secrets.ENCRYPTION_KEY)
    config.secrets.AWS_SECRET_ACCESS_KEY = decrypt(keys["AWS_SECRET_ACCESS_KEY"], config.secrets.ENCRYPTION_KEY)
    config.secrets.AWS_REGION = keys["AWS_REGION"]


    