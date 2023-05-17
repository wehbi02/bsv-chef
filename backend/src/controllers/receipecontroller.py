import os
import json
import random

from src.controllers.controller import Controller
from src.util.dao import DAO

from src.static.diets import Diet

class ReceipeController(Controller):
    def __init__(self, items_dao: DAO):
        super().__init__(dao=items_dao)

        # load existing receipes
        self.receipes = self.load_receipes()

    def load_receipes(self) -> list[dict]:
        """Read all available receipes from the src/static/receipes/ directory and puts them in an array. The items of this array follow the same format as the JSON files in the directory.
        
        returns:
          list of receipes in dictionary format"""
        receipes: list[dict] = []
        for filename in os.listdir('./src/static/receipes'):
            with open(f'./src/static/receipes/{filename}') as f:
                receipe = json.load(f)
                receipes.append(receipe)
        return receipes
    
    def filter_receipes(self, receipes: list[dict], diet: Diet) -> list[dict]:
        """Filters a list of receipes to contain only those that are available to the given diet.

        parameters:
          receipes -- list of receipes in JSON format, containing the "diets" field
          diet -- specified diet according to the Diet enumerator

        returns:
          subset of the receipes where every receipe is available to the given diet
        """
        filtered_receipes: list[dict] = []

        for receipe in receipes:
            if diet.name.lower() in receipe['diets']:
                filtered_receipes.append(receipe)

        return filtered_receipes
    
    def available_items(self) -> dict:
        """Obtain a list of available items in the pantry.
        
        returns:
          list of items available in the pantry mapped to their amount"""
        
        items = self.get_all()

        available_items = {}
        for item in items:
            available_items[item["name"]] = item["quantity"]

        return available_items
    
    def calculate_coverage(self, receipe: dict, available_items: dict) -> float:
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

        overall_coverage: float = sum(individual_coverages)/len(individual_coverages)

        return overall_coverage
    
    def get_coverage_of_receipes(self, receipes: list[dict], available_items: list[dict]) -> dict:
        """Calculate the coverage of each receipe by the available items.
        
        parameters:
          receipes -- list of receipes in the structure as found in src/static/receipes
          available_items -- list of available pantry items
          
        returns:
          A dictionary that maps a receipe name to a coverage value between 0 and 1 as calculated via calculate_coverage"""
        receipe_coverage = {}

        for receipe in receipes:
            coverage = self.calculate_coverage(receipe, available_items)
            receipe_coverage[receipe["name"]] = coverage

        return receipe_coverage

    def get_receipe(self, diet: Diet, take_best: bool) -> dict:
        """Propose a suitable receipe depending on the diet and the item usage strategy.
        
        parameters:
          diet -- A specification of a diet (available from the Diet enumerator) which the returned receipes must comply to.
          take_best -- Item usage strategy (True = Optimal, False = Random)
          
        returns:
          receipe -- A receipe in JSON format. The receipe complies to the dietary restrictions. If the usage strategy 'Optimal' has been selected (take_best == True) then the receipe with the highest coverage value as calculated in calculate_coverage will be returned - otherwise a random receipe will be returned."""

        available_receipes: list[dict] = self.filter_receipes(self.receipes, diet)
        available_items = self.available_items()

        # associate each receipe name with a coverage value
        receipe_coverage = self.get_coverage_of_receipes(receipes=available_receipes, available_items=available_items)

        # keep only those receipes which are at least partially covered
        filtered_receipes = {k:v for k,v in receipe_coverage.items() if v >= 0}
        if len(filtered_receipes) == 0:
            # no suitable receipes found
            return None

        # order the receipes in descending order according to the coverage values, i.e., the first receipe in the list is the one with the highest coverage value
        sorted_receipes = {k: v for k, v in sorted(filtered_receipes.items(), key=lambda item: item[1])}

        # determine which receipe to return according to the item usage mode
        selected_receipe_index = 0
        if not take_best: 
            selected_receipe_index = random.randint(0, len(sorted_receipes.keys())-1)
            
        # determine the receipe name and retrieve the receipe from the list of receipes to return it
        selected_receipe_name: str = list(sorted_receipes.keys())[selected_receipe_index]
        selected_receipe = [r for r in available_receipes if r['name']==selected_receipe_name][0]
        return selected_receipe