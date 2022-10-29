import glob
import os
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor

MODEL_DIR = 'fitted_models'
MODEL_CLASSES = {'Ridge': Ridge, 'RandomForestRegressor': RandomForestRegressor}


def restore_models(model_dir: str) -> dict:
    """
    Восстановление списка предобученных моделей.
    :param model_dir: папка с сохраненными моделями, относительный путь от корня запуска проекта.
    :return: Список предобученных моделей.
    """
    files = glob.glob(f'./{model_dir}/*')
    models = {}
    for file in files:
        models[file.split('/')[-1][:-4]] = file
    return models


if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

models_store = restore_models(MODEL_DIR)
