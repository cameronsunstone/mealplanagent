from collections import defaultdict
from typing import List
from schemas import Meal, ShoppingList, ShoppingListItem

CATEGORY_MAP = {
    "greek yogurt": "Dairy",
    "mixed berries": "Produce",
    "honey": "Pantry",
    "chicken breast": "Meat",
    "white rice": "Grains",
    "broccoli": "Produce",
}

def build_shopping_list(meals: List[Meal]) -> ShoppingList:
    agg = defaultdict(lambda: {"quantity": 0.0, "unit": "", "category": "Other"})
    for meal in meals:
        for ing in meal.ingredients:
            rec = agg[ing.name]
            rec["quantity"] += ing.quantity
            rec["unit"] = ing.unit or rec["unit"]
            rec["category"] = CATEGORY_MAP.get(ing.name.lower(), "Other")

    items = [
        ShoppingListItem(
            name=name,
            total_quantity=v["quantity"],
            unit=v["unit"],
            category=v["category"],
        )
        for name, v in agg.items()
    ]
    return ShoppingList(items=items)