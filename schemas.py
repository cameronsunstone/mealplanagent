from pydantic import BaseModel
from typing import List, Literal

class UserProfile(BaseModel):
    calories_min: int
    calories_max: int
    diet_type: Literal["omnivore", "vegetarian", "vegan", "keto"]
    allergies: List[str] = []
    dislikes: List[str] = []
    people: int = 1
    days: int = 7

class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: str

class Meal(BaseModel):
    name: str
    meal_type: Literal["breakfast", "lunch", "dinner"]
    ingredients: List[Ingredient]
    calories: int

class DayPlan(BaseModel):
    day: int
    meals: List[Meal]
    total_calories: int

class WeeklyPlan(BaseModel):
    user: UserProfile
    days: List[DayPlan]

class ShoppingListItem(BaseModel):
    name: str
    total_quantity: float
    unit: str
    category: str

class ShoppingList(BaseModel):
    items: List[ShoppingListItem]