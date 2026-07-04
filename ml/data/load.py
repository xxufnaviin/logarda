from utils.postgres import *
from datetime import datetime, timezone
import pandas as pd

def load_data(type:str, username = None):
    # create database engine
    engine = Postgres.create_engine()

    if type == "train":
        # select all metrics for training
        df_all = pd.read_sql("SELECT * FROM metrics", engine)
        cutoff = pd.Timestamp(datetime.now(timezone.utc).date()) - pd.Timedelta(weeks=8) # set train period

        # filter
        df = df_all[df_all['metrictime'] >= cutoff].reset_index(drop=True)

    elif type == "predict":
        # select only last one hour of data for prediction
        query = f"""WITH ranked AS (
                    SELECT *,
                        ROW_NUMBER() OVER (PARTITION BY instanceID ORDER BY metricTime DESC) AS num
                    FROM metrics WHERE username = '{username}')

                    SELECT metrictime, instanceid, cpu, network, memory, username FROM ranked WHERE num <= 24;""" # 24 data points
        
        df = pd.read_sql(query, engine)

    return df