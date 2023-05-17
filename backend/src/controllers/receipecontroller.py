import os
import json
import random

from src.controllers.controller import Controller
from src.util.dao import DAO

from src.static.diets import Diet
from src.util.calculator import calculate_readiness

class ReceipeController(Controller):
    def __init__(self, items_dao: DAO):
        super().__init__(dao=items_dao)

        # load existing receipes
        self.receipes = self.load_receipes()

    def load_receipes(self) -> list[dict]:
        """Read all available receipes from the src/static/receipes/ directory and puts them in an array. The items of this array follow the same format as the JSON files in the directory.

        returns:
          receipes -- list of receipes in dictionary format"""
        receipes: list[dict] = []
        for filename in os.listdir('./src/static/receipes'):
            with open(f'./src/static/receipes/{filename}') as f:
                receipe = json.load(f)
                receipes.append(receipe)
        return receipes

    def available_items(self) -> dict:
        """Obtain a list of available items in the pantry.

        returns:
          available_items -- list of items available in the pantry mapped to their amount"""

        items = self.get_all()

        available_items = {}
        for item in items:
            available_items[item["name"]] = item["quantity"]

        return available_items

    def get_receipe_readiness(self, receipe: dict, available_items: dict, diet: Diet) -> float:
        """Calculate the readiness value of a receipe. The readiness determines to what degree the required ingredients are already available in the current pantry.

        parameters:
          receipe -- a receipe in the structure as found in src/static/receipes
          available_items -- dictionary mapping all available pantry items to their currently available amount
          diet -- dietary preference which a receipe needs to comply to

        returns:
          readiness -- a value between 0 and 1 obtained via calculate_readiness and representing, how many of the required ingredients are already available
          None -- if the receipe has a current readiness of below 0.1
          None -- if the receipe is not available to the selected diet
        """
        if diet.name.lower() not in receipe['diets']:
            return None

        readiness = calculate_readiness(receipe, available_items)

        if readiness > 0.1:
            return readiness
        return None

    def get_readiness_of_receipes(self, receipes: list[dict], available_items: list[dict], diet: Diet) -> dict:
        """Calculate the readiness of each receipe by the available items.

        parameters:
          receipes -- list of receipes in the structure as found in src/static/receipes
          available_items -- list of available pantry items
          diet -- dietary preference which a receipe needs to comply to

        returns:
          readiness -- A dictionary that maps a receipe name (of receipes complying to the dietary restrictions) to a readiness value between 0 and 1 as calculated via calculate_readiness"""
        receipe_readiness = {}

        for receipe in receipes:
            readiness = self.get_receipe_readiness(
                receipe, available_items, diet)
            if readiness != None:
                receipe_readiness[receipe["name"]] = readiness

        return receipe_readiness

    def get_receipe(self, diet: Diet, take_best: bool) -> dict:
        """Propose a suitable receipe depending on the diet and the item usage strategy.

        parameters:
          diet -- A specification of a diet (available from the Diet enumerator) which the returned receipes must comply to.
          take_best -- Item usage strategy (True = Optimal, False = Random)

        returns:
          receipe -- A receipe in JSON format. The receipe complies to the dietary restrictions. If the usage strategy 'Optimal' has been selected (take_best == True) then the receipe with the highest readiness value as calculated in calculate_readiness will be returned - otherwise a random receipe will be returned."""

        available_items = self.available_items()

        # associate each receipe name with a readiness value
        receipe_readiness = self.get_readiness_of_receipes(
            receipes=self.receipes, available_items=available_items, diet=diet)
        if len(receipe_readiness.keys()) == 0: 
            return None

        # order the receipes in descending order according to the readiness values, i.e., the first receipe in the list is the one with the highest readiness value
        sorted_receipes = [k for k, v in sorted(
            receipe_readiness.items(), key=lambda item: item[0])]

        # determine which receipe to return according to the item usage mode
        selected_receipe_index = 0
        if not take_best:
            selected_receipe_index = random.randint(0, len(sorted_receipes)-1)

        # determine the receipe name and retrieve the receipe from the list of receipes to return it
        selected_receipe_name: str = sorted_receipes[selected_receipe_index]
        selected_receipe = [
            r for r in self.receipes if r['name'] == selected_receipe_name][0]
        return selected_receipe
