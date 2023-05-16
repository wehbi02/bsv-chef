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
                

    def get_receipe(self, diet: Diet, take_best: bool):
        available_receipes: list[dict] = self.filter_receipes(self.receipes, diet)
        available_items = self.available_items()

        receipe_coverage = {}
        for receipe in available_receipes:
            coverage = self.calculate_coverage(receipe, available_items)
            receipe_coverage[receipe["name"]] = coverage

        filtered_receipes = {k:v for k,v in receipe_coverage.items() if v>0}

        sorted_receipes = {k: v for k, v in sorted(filtered_receipes.items(), key=lambda item: item[0])}

        selected_receipe_index = 0
        if not take_best: 
            selected_receipe_index = random.randint(0, len(sorted_receipes.keys())-1)
            
        selected_receipe_name: str = list(sorted_receipes.keys())[selected_receipe_index]
        selected_receipe = [r for r in available_receipes if r['name']==selected_receipe_name][0]
        return selected_receipe