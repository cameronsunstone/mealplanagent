from schemas import UserProfile
from agents.orchestrator import run_full_pipeline


def demo():
    profile = UserProfile(
        calories_min=1800,
        calories_max=2200,
        diet_type="omnivore",
        allergies=["peanut"],
        dislikes=["kale"],
        people=2,
        days=7,
    )

    plan, nutrition_report, diet_report, shopping_list = run_full_pipeline(profile)

    print("=== Weekly Plan ===")
    for day in plan.days:
        print(f"Day {day.day} - {day.total_calories} kcal")
        for meal in day.meals:
            print(f"  {meal.meal_type:9}  {meal.name}")

    print("\n=== Nutrition Agent Report ===")
    print("OK:", nutrition_report["ok"])
    for msg in nutrition_report["messages"]:
        print(" -", msg)

    print("\n=== Diet Agent Report ===")
    print("OK:", diet_report["ok"])
    for v in diet_report["violations"]:
        print(" -", v)

    print("\n=== Shopping List ===")
    for item in shopping_list.items:
        print(
            f"{item.category:10} {item.name:20} "
            f"{item.total_quantity} {item.unit}"
        )


if __name__ == "__main__":
    demo()