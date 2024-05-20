import pytest
from unittest.mock import MagicMock
from src.controllers.recipecontroller import RecipeController
from src.static.diets import Diet

@pytest.fixture
def setup_controller():
    dao = MagicMock()
    controller = RecipeController(items_dao=dao)
    controller.recipes = [
        {"name": "Salad", "diets": ["vegan"], "ingredients": [{"name": "lettuce", "quantity": 1}]},
        {"name": "Pasta", "diets": ["vegetarian"], "ingredients": [{"name": "tomato", "quantity": 1}]},
        {"name": "Soup", "diets": ["vegetarian"], "ingredients": [{"name": "carrot", "quantity": 1}]},
        {"name": "Steak", "diets": ["none"], "ingredients": [{"name": "beef", "quantity": 1}]}
    ]
    return controller

def test_get_recipe_vegan_true(setup_controller):
    setup_controller.get_readiness_of_recipes = MagicMock(return_value={"Salad": 1.0})
    recipe = setup_controller.get_recipe(Diet.VEGAN, True)
    assert recipe == "Salad"

def test_get_recipe_vegan_false(setup_controller):
    setup_controller.get_readiness_of_recipes = MagicMock(return_value={"Salad": 1.0})
    recipe = setup_controller.get_recipe(Diet.VEGAN, False)
    assert recipe == "Salad"

def test_get_recipe_vegetarian_true(setup_controller):
    setup_controller.get_readiness_of_recipes = MagicMock(return_value={"Pasta": 0.8, "Soup": 0.9})
    recipe = setup_controller.get_recipe(Diet.VEGETARIAN, True)
    assert recipe in ["Pasta", "Soup"]

def test_get_recipe_vegetarian_false(setup_controller):
    setup_controller.get_readiness_of_recipes = MagicMock(return_value={"Pasta": 0.8, "Soup": 0.9})
    recipe = setup_controller.get_recipe(Diet.VEGETARIAN, False)
    assert recipe in ["Pasta", "Soup"]

def test_get_recipe_none_true(setup_controller):
    setup_controller.get_readiness_of_recipes = MagicMock(return_value={"Steak": 1.0})
    recipe = setup_controller.get_recipe(Diet.NONE, True)
    assert recipe == "Steak"

def test_get_recipe_none_false(setup_controller):
    setup_controller.get_readiness_of_recipes = MagicMock(return_value={"Steak": 1.0})
    recipe = setup_controller.get_recipe(Diet.NONE, False)
    assert recipe == "Steak"

def test_get_recipe_no_recipes(setup_controller):
    setup_controller.get_readiness_of_recipes = MagicMock(return_value={})
    recipe = setup_controller.get_recipe(Diet.VEGAN, True)
    assert recipe is None

def test_get_recipe_no_vegan_recipes(setup_controller):
    setup_controller.get_readiness_of_recipes = MagicMock(return_value={})
    recipe = setup_controller.get_recipe(Diet.VEGAN, True)
    assert recipe is None

def test_get_recipe_no_matching_recipes(setup_controller):
    setup_controller.get_readiness_of_recipes = MagicMock(return_value={})
    recipe = setup_controller.get_recipe(Diet.VEGETARIAN, True)
    assert recipe is None

def test_get_recipe_low_readiness(setup_controller):
    setup_controller.get_readiness_of_recipes = MagicMock(return_value={"Salad": 0.05, "Soup": 0.9})
    recipe = setup_controller.get_recipe(Diet.VEGETARIAN, True)
    assert recipe == "Soup"

