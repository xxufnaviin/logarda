# utility helper functions to abstract and moudlarize code


def generate_values(timestamp, metrics_data, instance):
    # database schema for table "metrics"
    metricTime = timestamp
    instanceID = instance
    cpu = round(metrics_data[timestamp]['cpu'],2)
    network = round(metrics_data[timestamp]['network_in'] + metrics_data[timestamp]['network_out'],2)
    memory = round(metrics_data[timestamp]['mem_used'],2)

    return [metricTime, instanceID, cpu, network, memory]