from typing import Tuple

from schemas import UserProfile, WeeklyPlan, DayPlan
from tools.recipe_db import get_recipes
from agents.nutrition_agent import run_nutrition_agent
from agents.diet_agent import run_diet_agent
from agents.shopping_agent import run_shopping_agent


def build_initial_plan(profile: UserProfile) -> WeeklyPlan:
    """
    Very simple planner that rotates through available recipes.

    It works even if there are only 1–2 recipes for a given diet type by
    reusing them via modulo. For the capstone, we only require at least
    ONE compatible recipe to build a plan.
    """
    recipes = get_recipes(profile.diet_type)

    # Only require at least one recipe; reuse it as needed.
    if len(recipes) == 0:
        raise ValueError("Need at least 1 recipe to build a plan.")

    days: list[DayPlan] = []

    # Simple rotation of meals for variety (or reuse).
    # We always pick three meals per day: breakfast, lunch, dinner.
    for i in range(profile.days):
        breakfast = recipes[i % len(recipes)]
        lunch = recipes[(i + 1) % len(recipes)]
        dinner = recipes[(i + 2) % len(recipes)]

        day_plan = DayPlan(
            day=i + 1,
            meals=[breakfast, lunch, dinner],
            total_calories=0,  # will be filled by the nutrition agent
        )
        days.append(day_plan)

    return WeeklyPlan(user=profile, days=days)


def run_meal_planner(profile: UserProfile) -> Tuple[WeeklyPlan, dict, dict]:
    """
    Orchestrator for planning only:
    - builds an initial weekly plan
    - runs the nutrition agent
    - runs the diet agent

    Returns:
        plan: WeeklyPlan
        nutrition_report: dict
        diet_report: dict
    """
    plan = build_initial_plan(profile)

    nutrition_report = run_nutrition_agent(plan, profile)
    diet_report = run_diet_agent(plan, profile)

    return plan, nutrition_report, diet_report


def run_full_pipeline(
    profile: UserProfile,
) -> Tuple[WeeklyPlan, dict, dict, object]:
    """
    High-level pipeline:
    - run the planner (orchestrator + nutrition + diet)
    - run the shopping list agent
    - return plan, reports, and shopping list

    Returns:
        plan: WeeklyPlan
        nutrition_report: dict
        diet_report: dict
        shopping_list: ShoppingList
    """
    plan, nutrition_report, diet_report = run_meal_planner(profile)
    shopping_list = run_shopping_agent(plan)
    return plan, nutrition_report, diet_report, shopping_list