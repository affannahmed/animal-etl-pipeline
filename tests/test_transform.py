import pytest
from src.transformation_logic import AnimalTransformer


def test_transform_friends_string():
    animal = {"friends": "dog,cat,bird"}
    result = AnimalTransformer.transform_animal(animal)
    assert result["friends"] == ["dog", "cat", "bird"]


def test_transform_friends_empty():
    animal = {"friends": ""}
    result = AnimalTransformer.transform_animal(animal)
    assert result["friends"] == []


def test_transform_born_at_integer():
    animal = {"born_at": 1609459200000}  # 2021-01-01
    result = AnimalTransformer.transform_animal(animal)
    assert "2021-01-01" in result["born_at"]
