def analyze_food_health(total_nutrients):
    calories = total_nutrients.get("calories", 0)
    fat = total_nutrients.get("fat", 0)
    sugar = total_nutrients.get("sugar", 0)
    sodium = total_nutrients.get("sodium", 0)

    # ✅ HEALTHY (very clean foods only)
    if (
        calories <= 300 and
        fat <= 8 and
        sodium <= 300
    ):
        return "Healthy"

    # 🔴 UNHEALTHY
    if (
        calories >= 650 or
        fat >= 25 or
        sodium >= 900
    ):
        return "Unhealthy"

    # 🟡 MODERATE (everything in between)
    return "Moderate"
def get_food_risk_from_dataset(food):
    import pandas as pd

    df = pd.read_csv("data/final_nutrition_dataset_balanced.csv")  # keep your file name

    food = food.lower().strip()

    # ✅ FIX: correct column name
    row = df[df["Food_Item"].str.lower().str.strip() == food]

    if row.empty:
        print("NOT FOUND:", food)  # debug
        return None

    return row.iloc[0]["nutrition_risk"]