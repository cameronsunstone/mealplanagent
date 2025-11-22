from schemas import UserProfile
from agents.orchestrator import run_full_pipeline


def run_evaluation():
    test_profiles = [
        UserProfile(
            calories_min=1800,
            calories_max=2200,
            diet_type="omnivore",
            allergies=["peanut"],
            dislikes=["kale"],
            people=2,
            days=7,
        ),
        UserProfile(
            calories_min=1600,
            calories_max=2000,
            diet_type="vegetarian",
            allergies=["peanut"],
            dislikes=[],
            people=1,
            days=5,
        ),
        UserProfile(
            calories_min=1400,
            calories_max=1900,
            diet_type="keto",
            allergies=[],
            dislikes=["rice"],
            people=1,
            days=3,
        ),
    ]

    for idx, profile in enumerate(test_profiles, start=1):
        plan, nutrition_report, diet_report, _ = run_full_pipeline(profile)

        print(f"\n=== Scenario {idx} ({profile.diet_type}) ===")
        print("Days:", len(plan.days))
        print("Nutrition OK:", nutrition_report["ok"])
        print("Diet OK:", diet_report["ok"])

        if not nutrition_report["ok"]:
            print("  Nutrition issues:")
            for msg in nutrition_report["messages"]:
                print("   -", msg)

        if not diet_report["ok"]:
            print("  Diet violations:")
            for v in diet_report["violations"]:
                print("   -", v)


if __name__ == "__main__":
    run_evaluation()