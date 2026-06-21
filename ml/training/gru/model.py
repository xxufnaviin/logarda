import pandas as pd
import tensorflow as tf
from keras.models import Sequential
from keras.layers import GRU, LSTM, Dense
import joblib

from ml.training.gru.preprocess import preprocess_data

def train_and_save(df_train:pd.DataFrame, df_validate:pd.DataFrame, df_test:pd.DataFrame, remove_cols):
    tf.keras.utils.set_random_seed(89)

    # split dataset into neural network based time series dataset
    train_dataset, validate_dataset, test_dataset, feature_size = preprocess_data(df_train, df_validate, df_test, remove_cols)

    # train model
    model = train_model(train_dataset, validate_dataset, feature_size)

    # save model
    save_model(model)


def train_model(train_dataset, validate_dataset, feature_size):
    model_gru = Sequential([
        GRU(32, input_shape=(12, feature_size)),
        Dense(32),
        Dense(3)
    ])

    model_gru.compile(
        optimizer = 'adam',
        loss=tf.keras.losses.LogCosh(),
        metrics=['mae']
    )

    model_gru.fit(train_dataset,validation_data=validate_dataset, epochs=30)

    return model_gru

def save_model(model):
    # save model to artifcats
    joblib.dump(model, "ml/artifacts/models/gru_model.pkl")