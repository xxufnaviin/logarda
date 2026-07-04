from datetime import datetime, timezone, timedelta
import pandas as pd

def train_val_test_split(tsdf:pd.DataFrame):
    current_date =datetime.now(timezone.utc).date() # get train date
    split_date_test = current_date - timedelta(days=10)
    split_date_validate = split_date_test - timedelta(days=6)

    df_train = tsdf[tsdf.metrictime < pd.to_datetime(split_date_validate)]
    df_validate = tsdf[(tsdf.metrictime >= pd.to_datetime(split_date_validate)) & (tsdf.metrictime < pd.to_datetime(split_date_test))]
    df_test = tsdf[tsdf.metrictime >= pd.to_datetime(split_date_test)]
    
    print("Split Percentage")
    print(f"Train Data: {len(df_train)/len(tsdf)*100:.2f} %")
    print(f"Validation Data: {len(df_validate)/len(tsdf)*100:.2f} %")
    print(f"Test Data: {len(df_test)/len(tsdf)*100:.2f} %")
    return df_train, df_validate, df_test
