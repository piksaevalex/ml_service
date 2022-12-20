import pytest
from unittest import mock
from app.db.models import Model
from app.module.logic import Logic
from app.module.model_classes import MODEL_CLASSES


@mock.patch('app.db.database.sessionmaker')
def test_get_model_classes_not_empty(mock_sessionmaker: mock.MagicMock):
    logic = Logic(mock_sessionmaker)
    assert len(logic.get_model_classes()) > 0


@mock.patch('app.db.database.sessionmaker')
def test_fit_model_bad_model_type_raise_exception(mock_sessionmaker: mock.MagicMock):
    logic = Logic(mock_sessionmaker)
    with pytest.raises(FileNotFoundError):
        logic.fit_model('Bad model type', {}, [], [])


@mock.patch('app.db.database.sessionmaker')
def test_fit_model_add_new_model(mock_sessionmaker: mock.MagicMock):
    model_class = list(MODEL_CLASSES.keys())[0]
    model_class_object = list(MODEL_CLASSES.values())[0]
    mock_sessionmaker.execute.return_value.fetchall.return_value = []

    logic = Logic(mock_sessionmaker)
    new_model = logic.fit_model(model_class, {}, [[1, 2, 3], [2, 2, 3], [3, 2, 1]], [1, 2, 3])

    assert new_model['model_type'] == str(model_class)
    assert new_model['model_name'] == str(model_class_object())


@mock.patch('app.db.database.sessionmaker')
def test_fit_model_refit_exist_model(mock_sessionmaker: mock.MagicMock):
    model_class = list(MODEL_CLASSES.keys())[0]
    model_class_object = list(MODEL_CLASSES.values())[0]
    mock_exist_object = Model(id=1, model_type=str(model_class), model_name=str(model_class_object()), model_data=b'')
    mock_sessionmaker.execute.return_value.fetchall.return_value = [mock_exist_object]

    logic = Logic(mock_sessionmaker)
    new_model = logic.fit_model(model_class, {}, [[1, 2, 3], [2, 2, 3], [3, 2, 1]], [1, 2, 3])

    assert new_model['id'] == mock_exist_object.id
    assert new_model['model_type'] == mock_exist_object.model_type
    assert new_model['model_name'] == mock_exist_object.model_name
