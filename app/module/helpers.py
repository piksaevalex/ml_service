import glob


def restore_models(model_dir):
    files = glob.glob(f'./{model_dir}/*')
    models_store = {}
    for file in files:
        models_store[file.split('/')[-1][:-4]] = file
    return models_store
