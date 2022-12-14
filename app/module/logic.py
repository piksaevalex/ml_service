import pickle
import numpy as np
from app.db.models import Model
from sqlalchemy.orm import sessionmaker
from app.module.model_classes import MODEL_CLASSES


class Logic:
    def __init__(self, db_provider: sessionmaker):
        self.db_provider = db_provider

    @staticmethod
    def get_model_classes():
        return list(MODEL_CLASSES.keys())

    def get_models(self):
        with self.db_provider() as db:
            items = db.query(Model).all()
            items = [e.serialize() for e in items]
        return items

    def fit_model(self, model_type: str, params: dict, x: list, y: list) -> dict:
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
        model_bytes = pickle.dumps(model, 0)

        with self.db_provider() as db:
            model = db.query(Model).filter(Model.model_name == model_name).first()
            if not model:
                model = Model(model_type=model_type, model_name=model_name, model_data=model_bytes)
                db.add(model)
                db.commit()
                db.refresh(model)
                model = model.serialize()
            else:
                model.model_data = model_bytes
                db.commit()
                model = model.serialize()
        return model

    def predict_model(self, model_id: int, x: list) -> list:
        """
        Предсказание предобученой моделью.
        :param model_id: Название модели.
        :param x: Выборка признаков.
        :return: Предсказанные значения.
        """
        with self.db_provider() as db:
            model = db.query(Model).filter(Model.id == model_id).first()
            if not model:
                raise FileNotFoundError('Данная модель не найдена')
            model = pickle.loads(model.model_data)

        y_pred = model.predict(x)
        return y_pred.tolist()

    def delete_model(self, model_id: str) -> None:
        """
        Удалить модель.
        :param model_id: Название модели.
        :return: None
        """
        with self.db_provider() as db:
            model_query = db.query(Model).filter(Model.id == model_id)
            model = model_query.first()
            if not model:
                raise FileNotFoundError('Данная модель не найдена')
            model_query.delete(synchronize_session='False')
            db.commit()
