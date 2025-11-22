from typing import Tuple
from schemas import (
    UserProfile,
    WeeklyPlan,
    DayPlan,
)
from tools.recipe_db import get_recipes
from agents.nutrition_agent import run_nutrition_agent
from agents.diet_agent import run_diet_agent
from agents.shopping_agent import run_shopping_agent


def build_initial_plan(profile: UserProfile) -> WeeklyPlan:
    """
    Very simple 'planner' that just rotates through available recipes.
    In the ADK version, this is where your LLM-powered planner would live.
    """
    recipes = get_recipes(profile.diet_type)
    if len(recipes) < 3:
        raise ValueError("Need at least 3 recipes to build a plan.")

    days = []
    # Simple rotation of meals for variety
    for i in range(profile.days):
        # pick three recipes by index so they rotate
        breakfast = recipes[i % len(recipes)]
        lunch = recipes[(i + 1) % len(recipes)]
        dinner = recipes[(i + 2) % len(recipes)]

        day_plan = DayPlan(
            day=i + 1,
            meals=[breakfast, lunch, dinner],
            total_calories=0,  # will be filled by nutrition agent
        )
        days.append(day_plan)

    return WeeklyPlan(user=profile, days=days)


def run_meal_planner(profile: UserProfile) -> Tuple[WeeklyPlan, dict, dict]:
    """
    Orchestrator 'agent':
    - builds an initial plan
    - sends to nutrition agent
    - sends to diet agent
    - (optionally could loop to fix issues)
    - returns plan and agent reports
    """
    plan = build_initial_plan(profile)

    nutrition_report = run_nutrition_agent(plan, profile)
    diet_report = run_diet_agent(plan, profile)

    # If you want to be fancy, you can add a loop here that
    # regenerates the plan if nutrition_report["ok"] or
    # diet_report["ok"] is False. For now, just return reports.

    return plan, nutrition_report, diet_report


def run_full_pipeline(profile: UserProfile):
    """
    High-level convenience function:
    orchestrator + shopping list agent.
    """
    plan, nutrition_report, diet_report = run_meal_planner(profile)
    shopping_list = run_shopping_agent(plan)
    return plan, nutrition_report, diet_report, shopping_list