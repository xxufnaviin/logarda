import pandas as pd
from scipy.stats.mstats import winsorize


def clean_dataset(df:pd.DataFrame):
    tsdf = winsorizeValues(df)
    tsdf = createGroupedIdentity(tsdf, "username", "instanceid")
    tsdf = dropIrrelevantColumns(tsdf)
    tsdf = createLagFeatures(tsdf, lags=3, instancegroup="instance_group")
    tsdf = sortData(tsdf)
    
    return tsdf

# cap extreme values
def winsorizeValues(tsdf: pd.DataFrame, cols = ["cpu","network","memory"]):
    for col in cols:
        tsdf[col] = winsorize(tsdf[col],limits=[0.005, 0.005])
    return tsdf

# merge username and instance id as one
def createGroupedIdentity(tsdf: pd.DataFrame, username:str, instance:str):
    tsdf["instance_group"] = tsdf[username]+ "_" + tsdf[instance]
    return tsdf

# drop username and instanceid after emrging them
def dropIrrelevantColumns(tsdf:pd.DataFrame):
    tsdf = tsdf.drop(["username", "instanceid"], axis =1)
    return tsdf

# set time as the index column and sort values
def sortData(tsdf:pd.DataFrame):
    tsdf = tsdf.sort_values(["instance_group","metrictime"],ascending=[True, True]).reset_index(drop=True)
    return tsdf

# feature creation for lag windows and rolling average
def createLagFeatures(tsdf: pd.DataFrame, lags: int, instancegroup:str):
    tsdf = tsdf.sort_values("metrictime").reset_index(drop=True)
    columns = tsdf.columns
    for col in columns:
        if not pd.api.types.is_numeric_dtype(tsdf[col]):
            continue
        for lag in range(1, lags + 1):
            tsdf[f"{col}_lag-{lag}"] = tsdf.groupby(instancegroup)[col].shift(lag) # create lag features for history
    # Create lag features for each column

    return tsdf
