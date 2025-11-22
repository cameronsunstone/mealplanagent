from typing import Dict, List
from schemas import WeeklyPlan, UserProfile

MEAT_INGREDIENTS = [
    "chicken",
    "beef",
    "pork",
    "bacon",
    "salmon",
    "fish",
    "steak",
]


def run_diet_agent(plan: WeeklyPlan, profile: UserProfile) -> Dict:
    """
    Simple rule-based diet checker.
    In your ADK version, this is where you'd call the LLM.
    """
    violations: List[str] = []
    ok = True

    for day in plan.days:
        for meal in day.meals:
            for ing in meal.ingredients:
                name = ing.name.lower()

                # allergies & dislikes
                for allergen in profile.allergies:
                    if allergen.lower() in name:
                        ok = False
                        violations.append(
                            f"Day {day.day}: {meal.name} contains "
                            f"allergen '{allergen}' in ingredient '{ing.name}'."
                        )

                for dislike in profile.dislikes:
                    if dislike.lower() in name:
                        ok = False
                        violations.append(
                            f"Day {day.day}: {meal.name} contains "
                            f"disliked ingredient '{dislike}'."
                        )

                # basic vegetarian/vegan checks
                if profile.diet_type in ("vegetarian", "vegan"):
                    if any(m in name for m in MEAT_INGREDIENTS):
                        ok = False
                        violations.append(
                            f"Day {day.day}: {meal.name} is not "
                            f"{profile.diet_type} due to '{ing.name}'."
                        )

                # basic keto check (very naive)
                if profile.diet_type == "keto":
                    if "rice" in name or "quinoa" in name or "bread" in name:
                        ok = False
                        violations.append(
                            f"Day {day.day}: {meal.name} may be too high-carb "
                            f"for keto due to '{ing.name}'."
                        )

    if ok:
        violations.append("No diet violations detected.")

    return {
        "ok": ok,
        "violations": violations,
    }