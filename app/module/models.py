import pickle
import numpy as np
import os
from .helpers import restore_models
from sklearn.linear_model import *
from sklearn.ensemble import RandomForestRegressor

model_dir = 'fitted_models'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

Model_classes = ['Ridge', 'RandomForestRegressor']
models_store = restore_models(model_dir)


def fit_model(model_type, params, x, y):
    x = np.array(x)
    y = np.array(y)
    model = eval(model_type)(**params)
    model.fit(x, y)
    with open(os.path.join(model_dir, f'{model.__str__()}.pkl'), 'wb') as f:
        pickle.dump(model, f)

    models_store[model.__str__()] = os.path.join(model_dir, f'{model.__str__()}.pkl')


def predict_model(model_name, x):
    model_name_path = models_store[model_name]
    with open(model_name_path, 'rb') as f:
        model = pickle.load(f)

    y_pred = model.predict(x)
    return y_pred


def delete_model(model_name):
    try:
        model_path = models_store[model_name]
        os.remove(model_path)
        del models_store[model_name]
    except KeyError:
        raise KeyError('Данная модель не найдена')
