import glob


def restore_models(model_dir: str) -> dict:
    """
    Восстановление списка предобученных моделей.
    :param model_dir: папка с сохраненными моделями, относительный путь от корня запуска проекта.
    :return: Список предобученных моделей.
    """
    files = glob.glob(f'./{model_dir}/*')
    models_store = {}
    for file in files:
        models_store[file.split('/')[-1][:-4]] = file
    return models_store
