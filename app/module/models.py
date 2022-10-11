import pickle
import numpy as np
import os
from .helpers import restore_models
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor

model_dir = 'fitted_models'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

Model_classes = ['Ridge', 'RandomForestRegressor']
models_store = restore_models(model_dir)


def fit_model(model_type: str, params: dict, x: list, y: list) -> str:
    """
    Обучает модель.
    :param model_type: Тип модели.
    :param params: Гиперпараметры модели.
    :param x: Обчающая выборка (признаки).
    :param y: Таргет обучающей выборки.
    :return: Имя обученной модели
    """
    x = np.array(x)
    y = np.array(y)
    model = eval(model_type)(**params)
    model.fit(x, y)
    model_name = model.__str__()
    with open(os.path.join(model_dir, f'{model_name}.pkl'), 'wb') as f:
        pickle.dump(model, f)

    models_store[model_name] = os.path.join(model_dir, f'{model_name}.pkl')
    return model_name


def predict_model(model_name: str, x: list) -> list:
    """
    Предсказание предобученой моделью.
    :param model_name: Название модели.
    :param x: Выборка признаков.
    :return: Предсказанные значения.
    """
    try:
        model_name_path = models_store[model_name]
        with open(model_name_path, 'rb') as f:
            model = pickle.load(f)
    except KeyError:
        raise KeyError('Данная модель не найдена')

    y_pred = model.predict(x)
    return y_pred.tolist()


def delete_model(model_name: str) -> None:
    """
    Удалить модель.
    :param model_name: Название модели.
    :return: None
    """
    try:
        model_path = models_store[model_name]
        os.remove(model_path)
        del models_store[model_name]
    except KeyError:
        raise KeyError('Данная модель не найдена')
