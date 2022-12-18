import pytest
from app.module.logic import get_model_classes, fit_model
from app.module.model_classes import MODEL_CLASSES


def test_get_model_classes_not_empty():
    assert len(get_model_classes()) > 0


def test_fit_model_bad_model_type_raise_exception():
    with pytest.raises(FileNotFoundError):
        fit_model('Bad model type', {}, [], [])


# def test_fit_model():
#     model_class = list(MODEL_CLASSES.keys())[0]
#     fit_model(model_class, {}, [[1, 2, 3], [2, 2, 3], [3, 2, 1]], [1, 2, 3])
