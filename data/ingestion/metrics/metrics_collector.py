from utils.postgres import *
from utils.aws import *
from utils.utils import *


# establish connection with cloudwatch and ec2      
cloudwatch = Cloudwatch_Client()
ec2 = EC2_Client()

# establish connection with PostgreSQL database
conn = Postgres.create_connection()

if __name__ == "__main__":
    print("Collecting new metrics!")
    # get metrics data for each instance
    for instance, host in ec2.all_instances:
        metrics_data, data_exists = cloudwatch.get_metrics(instance, host)
        
        if data_exists:
            for timestamp in metrics_data:
                # generate values for each field
                metric_values = generate_metric_values(timestamp, metrics_data, instance)

                # insert into database one row at a time
                Postgres.insert_data(conn, metric_values, data="metrics")
        else:
            pass

    conn.close()