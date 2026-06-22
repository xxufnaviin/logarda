import pandas as pd
import numpy as np
from keras.preprocessing import timeseries_dataset_from_array

def preprocess_data(df_train:pd.DataFrame, df_validate:pd.DataFrame, df_test:pd.DataFrame, columns_to_remove):
    X = [x for x in df_train.columns if "target" not in x]
    time = ["hour", "day", "day_of_week", "minute"]

    # train data features
    X_train = df_train[X]
    X_train = X_train.drop(columns_to_remove, axis = 1)

    dl_columns = [x for x in X_train.columns if "lag" not in x and "diff" not in x and "average" not in x and "group" not in x][3:] 
    dl_columns = ["target_cpu","target_memory","target_network"] + [x for x in dl_columns if x not in time] 

    feature_size = len(dl_columns)

    train_data = df_train[dl_columns].values
    test_data = df_test[dl_columns].values
    validate_data = df_validate[dl_columns].values
    
    return create_nn_dataset(train_data, validate_data, test_data, feature_size)


def create_nn_dataset(train_data, validate_data, test_data, feature_size):
    lookback = 12 # how many steps to look back, 12 for 5-minute itnervals is 1 hour roughly

    # split data, for features use all
    # for y use the target features = cpu, network, memory (first three columns)
    train_X = train_data
    train_y = train_data[lookback:,:3] # all rows, first three columns (shape = (rows, columns))

    test_X = test_data
    test_y = test_data[lookback:,:3]

    validate_X = validate_data
    validate_y = validate_data[lookback:,:3]

    train_X = train_X.astype(np.float32)
    test_X = test_X.astype(np.float32)
    validate_X = validate_X.astype(np.float32)

    train_y = train_y.astype(np.float32)
    test_y = test_y.astype(np.float32)
    validate_y = validate_y.astype(np.float32)

    train_dataset = timeseries_dataset_from_array(
    data=train_X,
    targets=train_y,
    sequence_length=lookback,
    batch_size=32
    )

    test_dataset = timeseries_dataset_from_array(
        data=test_X,
        targets=test_y,
        sequence_length=lookback,
        batch_size=32
    )

    validate_dataset = timeseries_dataset_from_array(
        data=validate_X,
        targets=validate_y,
        sequence_length=lookback,
        batch_size=32
    )

    return train_dataset, validate_dataset, test_dataset, feature_size
