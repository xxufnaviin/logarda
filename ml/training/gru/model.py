import pandas as pd
import tensorflow as tf
from keras.models import Sequential
from keras.layers import GRU, LSTM, Dense
import joblib

from ml.training.gru.preprocess import preprocess_data

def train_and_save(df_train:pd.DataFrame, df_validate:pd.DataFrame, df_test:pd.DataFrame, remove_cols):
    tf.keras.utils.set_random_seed(89)

    # split dataset into neural network based time series dataset
    train_dataset, validate_dataset, feature_size, features = preprocess_data(df_train, df_validate, df_test, remove_cols)

    # train model
    model = train_model(train_dataset, validate_dataset, feature_size)

    # save model
    save_model(model)

    return features


def train_model(train_dataset, validate_dataset, feature_size):
    model_gru = Sequential([
        GRU(64, input_shape=(12, feature_size)), # 3 because 3 inputs only (pre-feature engineered)
        Dense(32),
        Dense(3)
    ])

    model_gru.compile(
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.0003),
        loss=tf.keras.losses.LogCosh(),
        metrics=['mae']
    )
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    )

    model_gru.fit(train_dataset,validation_data=validate_dataset, callbacks=[early_stop], epochs=30)

    return model_gru

def save_model(model):
    # save model to artifcats
    joblib.dump(model, "ml/artifacts/models/gru_model.pkl")