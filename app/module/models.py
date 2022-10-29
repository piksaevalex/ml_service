import pickle
import numpy as np
import os
from .storage import MODEL_CLASSES, MODEL_DIR, models_store


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
    model = MODEL_CLASSES.get(model_type)
    if model is None:
        raise FileNotFoundError('Данная модель не найдена, '
                                'используйте GET model_classes для получения доступных моделей')
    model = model(**params)
    model.fit(x, y)
    model_name = model.__str__()
    with open(os.path.join(MODEL_DIR, f'{model_name}.pkl'), 'wb') as f:
        pickle.dump(model, f)

    models_store[model_name] = os.path.join(MODEL_DIR, f'{model_name}.pkl')
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
        raise FileNotFoundError('Данная модель не найдена')

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
        raise FileNotFoundError('Данная модель не найдена')
