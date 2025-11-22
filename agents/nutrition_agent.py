from typing import Dict, List
from schemas import WeeklyPlan, UserProfile
from tools.nutrition_tools import daily_calories


def run_nutrition_agent(plan: WeeklyPlan, profile: UserProfile) -> Dict:
    """
    Check that each day's calories are within the profile's target range.
    Returns a small report dict.
    """
    per_day: List[int] = []
    messages: List[str] = []
    ok = True

    for day in plan.days:
        total = daily_calories(day.meals)
        per_day.append(total)
        if total < profile.calories_min:
            ok = False
            messages.append(
                f"Day {day.day} is below target: {total} kcal "
                f"(min {profile.calories_min})."
            )
        elif total > profile.calories_max:
            ok = False
            messages.append(
                f"Day {day.day} is above target: {total} kcal "
                f"(max {profile.calories_max})."
            )

        # keep the data on the plan object too
        day.total_calories = total

    if ok:
        messages.append("All days within calorie range.")

    return {
        "ok": ok,
        "per_day_calories": per_day,
        "messages": messages,
    }