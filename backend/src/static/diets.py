from enum import Enum

class Diet(Enum):
    NORMAL = 1
    VEGETARIAN = 2
    VEGAN = 3

def from_string(input: str) -> Diet:
    """Convert a string input into an appropriate enum value.
    
    parameters:
      input -- the input string to be converted
      
    returns:
      Diet.VEGETARIAN -- if the string resembles "vegetarian"
      Diet.VEGAN -- if the string resembles "vegan"
      Diet.NORMAL -- otherwise"""
    
    if input.lower() in ['vegetarian']:
        return Diet.VEGETARIAN
    elif input.lower() in ['vegan']:
        return Diet.VEGAN
    return Diet.NORMAL