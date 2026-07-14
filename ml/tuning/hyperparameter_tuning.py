from itertools import product

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from skforecast.metrics import symmetric_mean_absolute_percentage_error


def tune_model(model_class, X_train, y_train, X_val, y_val, target, scaler_y, param_grid,):
    keys = list(param_grid.keys())
    values = list(param_grid.values())

    best_score = float("inf")
    best_params = None
    results = []

    for combination in product(*values):

        params = dict(zip(keys, combination))

        model = model_class(**params)

        model.fit(X_train, y_train)

        y_pred = model.predict(X_val)

        smape = evaluate_target(y_pred=y_pred, y_true=y_val, target=target,scaler_y=scaler_y)

        results.append({"params": params, "smape": smape})

        if smape < best_score:
            best_score = smape
            best_params = params

    return best_params, best_score, results


def evaluate_target(y_pred, y_true, target, scaler_y):
    columns = scaler_y.get_feature_names_out()
    # Create dataframe with all targets
    pred_df = pd.DataFrame(np.zeros((len(y_pred), 3)),columns=columns)

    true_df = pd.DataFrame(np.zeros((len(y_true), 3)),columns=columns)

    # Insert target prediction/value
    pred_df[target] = y_pred
    true_df[target] = y_true.values

    # Inverse scaling
    pred_df = pd.DataFrame(scaler_y.inverse_transform(pred_df),columns=columns)

    true_df = pd.DataFrame(scaler_y.inverse_transform(true_df),columns=columns)

    # Reverse log transform
    pred_df[target] = np.expm1(pred_df[target])

    true_df[target] = np.expm1(true_df[target])

    # Calculate sMAPE
    smape = symmetric_mean_absolute_percentage_error(true_df[target],pred_df[target])

    return smape
