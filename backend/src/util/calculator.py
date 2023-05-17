def calculate_readiness(receipe: dict, available_items: dict) -> float:
    """Calculate the readiness of ingredients by the available pantry items. The readiness is calculated as the average of all ingredients, i.e., each ingredient can be ready between 0% (ingredient not available) to 100% (i.e., 100% of the required amount of the ingredient is available in the pantry). The overall readiness is the average between the individual readiness of all required ingredients.

    parameters:
        receipe -- receipe of interest containing a list of required ingredients
        available_items -- list of items available in the pantry

    returns:
        A readiness value, where a value of 1 (=100%) means that all items required for the receipe are available in the pantry, a readiness of 0 means none of the items are available."""

    required_ingredients = receipe['ingredients']
    individual_readiness = []
    for required_ingredient, required_amount in required_ingredients.items():

        individual_readiness: float = 0
        if required_ingredient in list(available_items.keys()):
            available_amount = available_items.get(required_ingredient)
            individual_readiness = min(1, available_amount/required_amount)
        individual_readiness.append(individual_readiness)

    overall_coverage: float = sum(
        individual_readiness)/len(individual_readiness)

    return overall_coverage