from utils.postgres import *
import pandas as pd

def load_data(type:str, username = None):
    # create database engine
    engine = Postgres.create_engine()

    if type == "train":
        # select all metrics for training
        df = pd.read_sql("SELECT * FROM metrics", engine)

    elif type == "predict":
        # select only last one hour of data for prediction
        query = f"""WITH ranked AS (
                    SELECT *,
                        ROW_NUMBER() OVER (PARTITION BY instanceID ORDER BY metricTime DESC) AS num
                    FROM metrics WHERE username = '{username}')

                    SELECT metrictime, instanceid, cpu, network, memory, username FROM ranked WHERE num <= 24;""" # 24 data points
        
        df = pd.read_sql(query, engine)

    return df