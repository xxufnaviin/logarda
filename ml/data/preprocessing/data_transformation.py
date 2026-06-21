import pandas as pd

def preprocess_dataset(df_train:pd.DataFrame, df_validate:pd.DataFrame, df_test:pd.DataFrame):
    df_train = createRollingFeatures(df_train, rolling_window = 3, instancegroup="instance_group")
    df_train = setTimeIndex(df_train, "metrictime")
    df_train = createTimeFeatures(df_train)
    df_train = df_train.dropna()

    df_test = createRollingFeatures(df_test, rolling_window = 3, instancegroup="instance_group")
    df_test = setTimeIndex(df_test, "metrictime")
    df_test = createTimeFeatures(df_test)
    df_test = df_test.dropna()

    df_validate = createRollingFeatures(df_validate, rolling_window = 3, instancegroup="instance_group")
    df_validate = setTimeIndex(df_validate, "metrictime")
    df_validate = createTimeFeatures(df_validate)
    df_validate = df_validate.dropna()
    
    return df_train, df_validate, df_test

def preprocess_data(df_predict:pd.DataFrame):
    df_predict = createRollingFeatures(df_predict, rolling_window = 3, instancegroup="instance_group")
    df_predict = setTimeIndex(df_predict, "metrictime")
    df_predict = createTimeFeatures(df_predict)
    df_predict = df_predict.dropna()

    return df_predict


def createRollingFeatures(tsdf: pd.DataFrame, rolling_window:int, instancegroup:str):
    columns = ["cpu", "network", "memory"]
    for col in columns:
        if not pd.api.types.is_numeric_dtype(tsdf[col]):
            continue
        tsdf[f"{col}_rolling_average"] = tsdf.groupby(instancegroup)[col].transform(lambda x: x.rolling(rolling_window).mean())#.reset_index(drop=True)
    # Create rolling average features based on a rolling window

    for col in columns:
        if not pd.api.types.is_numeric_dtype(tsdf[col]):
            continue
        tsdf[f"{col}_rolling_std"] = tsdf.groupby(instancegroup)[col].transform(lambda x: x.rolling(rolling_window+2).std())#.reset_index(drop=True)
    # Create rolling std features based on a rolling window

    for col in columns:
        if not pd.api.types.is_numeric_dtype(tsdf[col]):
            continue
        tsdf[f"{col}_diff"] = tsdf.groupby(instancegroup)[col].transform(lambda x: x.diff())#.reset_index(drop=True)
    # Create diff features based on a rolling window

    for col in columns:
        if not pd.api.types.is_numeric_dtype(tsdf[col]):
            continue
        tsdf[f"{col}_rolling_max"] = tsdf.groupby(instancegroup)[col].transform(lambda x: x.rolling(rolling_window+2).max())#.reset_index(drop=True)
    # Create rolling average features based on a rolling window


    for col in columns:
        if not pd.api.types.is_numeric_dtype(tsdf[col]):
            continue
        tsdf[f"target_{col}"] = tsdf.groupby(instancegroup)[col].shift(-1)#.reset_index(drop=True) # create a future value for target prediction

    return tsdf

# set time as the index column and sort values
def setTimeIndex(tsdf:pd.DataFrame, timeindex:str):
    tsdf = tsdf.sort_values(["instance_group","metrictime"],ascending=[True, True]).reset_index(drop=True).set_index(timeindex)
    return tsdf

# create time-based features for each row
def createTimeFeatures(tsdf: pd.DataFrame):
    tsdf["hour"] = tsdf.index.hour
    tsdf["day"] = tsdf.index.day
    tsdf["day_of_week"] = tsdf.index.dayofweek
    tsdf["is_weekend"] = tsdf.index.dayofweek >= 5
    tsdf["minute"] = tsdf.index.minute

    return tsdf