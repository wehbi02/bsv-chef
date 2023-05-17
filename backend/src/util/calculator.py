def calculate_coverage(receipe: dict, available_items: dict) -> float:
    """Calculate the coverage of ingredients by the available pantry items. The covererage is calculated as the average of all ingredients, i.e., each ingredient can be covered between 0% (ingredient not available) to 100% (i.e., 100% of the required amount of the ingredient is available in the pantry). The overall coverage is the average between the individual coverage of all required ingredients.

    parameters:
        receipe -- receipe of interest containing a list of required ingredients
        available_items -- list of items available in the pantry

    returns:
        A coverage value, where a value of 1 (=100%) means that all items required for the receipe are available in the pantry, a coverage of 0 means none of the items are available."""

    required_ingredients = receipe['ingredients']
    individual_coverages = []
    for required_ingredient, required_amount in required_ingredients.items():

        individual_coverage: float = 0
        if required_ingredient in list(available_items.keys()):
            available_amount = available_items.get(required_ingredient)
            individual_coverage = min(1, available_amount/required_amount)
        individual_coverages.append(individual_coverage)

    overall_coverage: float = sum(
        individual_coverages)/len(individual_coverages)

    return overall_coverage