def calculate_readiness(recipe: dict, available_items: dict) -> float:
    """Calculate the readiness of ingredients by the available pantry items. The readiness is calculated as the average of all ingredients, i.e., each ingredient can be ready between 0% (ingredient not available) to 100% (i.e., 100% of the required amount of the ingredient is available in the pantry). The overall readiness is the average between the individual readiness of all required ingredients.

    parameters:
        recipe -- recipe of interest containing a list of required ingredients
        available_items -- list of items available in the pantry

    returns:
        A readiness value, where a value of 1 (=100%) means that all items required for the recipe are available in the pantry, a readiness of 0 means none of the items are available."""

    required_ingredients = recipe['ingredients']
    for required_ingredient, required_amount in required_ingredients.items():
        individual_readiness = []

        ingredient_readiness: float = 0
        if required_ingredient in list(available_items.keys()):
            available_amount = available_items.get(required_ingredient)
            ingredient_readiness = calculate_ingredient_readiness(available_amount, required_amount)
        individual_readiness.append(ingredient_readiness)

    overall_readiness: float = sum(
        individual_readiness)/len(individual_readiness)

    return overall_readiness

def calculate_ingredient_readiness(available_amount, required_amount):
    """Calculate the readiness of one ingredient

    parameters:
        available_amount -- amount that is available of this ingredient
        required amount -- amount that is required of this ingredient for the recipe

    returns:
        0 -- if the required amount is 0
        ingredient readiness -- value between 0 (ingredient is unavailable) to 1 (the available amount of the ingredient is as least as high as the required)
    """
    if required_amount == 0:
        return 0
    return min(1, available_amount/required_amount)