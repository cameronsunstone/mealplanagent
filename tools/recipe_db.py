import json
from pathlib import Path
from typing import List
from schemas import Meal, Ingredient

DATA_PATH = Path(__file__).parent.parent / "data" / "recipes.json"

with open(DATA_PATH) as f:
    RAW_RECIPES = json.load(f)

def get_recipes(diet_type: str) -> List[Meal]:
    """Return recipes compatible with the given diet_type."""
    filtered = []
    for r in RAW_RECIPES:
        if diet_type == "omnivore" or diet_type in r.get("diet_tags", []):
            ingredients = [Ingredient(**ing) for ing in r["ingredients"]]
            filtered.append(
                Meal(
                    name=r["name"],
                    meal_type=r["meal_type"],
                    ingredients=ingredients,
                    calories=r["calories"],
                )
            )
    return filtered