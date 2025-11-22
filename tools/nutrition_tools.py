from typing import List
from schemas import Meal

def daily_calories(meals: List[Meal]) -> int:
    return sum(m.calories for m in meals)