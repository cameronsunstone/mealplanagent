from schemas import WeeklyPlan, ShoppingList
from tools.shopping_tools import build_shopping_list


def run_shopping_agent(plan: WeeklyPlan) -> ShoppingList:
    """
    Build a consolidated shopping list from the weekly plan.
    """
    all_meals = []
    for day in plan.days:
        all_meals.extend(day.meals)

    shopping_list = build_shopping_list(all_meals)
    return shopping_list