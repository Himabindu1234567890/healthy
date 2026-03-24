import pandas as pd
import json

# -------------------------------
# LOAD DATASET
# -------------------------------
df = pd.read_csv("data/final_nutrition_dataset_balanced.csv")

# 🔥 Normalize dataset once (IMPORTANT FIX)
df["Food_Item"] = df["Food_Item"].str.strip().str.lower()

# -------------------------------
# LOAD FOOD-UNIT MAPPING
# -------------------------------
with open("data/portion_mapping.json") as f:
    PORTION_MAP = json.load(f)
PORTION_MAP = {
    k.strip().lower(): {uk.strip().lower(): uv for uk, uv in v.items()}
    for k, v in PORTION_MAP.items()
}


# =========================================================
# EXISTING FUNCTIONS (SAFE VERSION)
# =========================================================

def get_food_list():
    # Return original formatted names (capitalize for UI)
    return sorted(df["Food_Item"].str.title().unique())


def calculate_grams(food, unit, count):
    if not food or not unit or not count:
        return 0

    food = food.strip().lower()
    unit = unit.strip().lower()

    # ✅ DIRECT GRAMS
    if unit == "grams":
        return float(count)

    # ✅ USE MAPPING
    if food in PORTION_MAP and unit in PORTION_MAP[food]:
        return PORTION_MAP[food][unit] * float(count)

    # ⚠️ FALLBACK
    print("⚠️ No mapping for:", food, unit)
    return 100 * float(count)


def get_nutrients(food, grams):

    if grams == 0:
        return {
            "calories": 0,
            "protein": 0,
            "carbohydrates": 0,
            "fat": 0,
            "fiber": 0,
            "sugar": 0,
            "sodium": 0
        }

    # 🔥 Normalize food name before matching
    food = food.strip().lower()

    row = df[df["Food_Item"].apply(lambda x: food in x)]

    # -------------------------
    # CASE 1: FOOD EXISTS
    # -------------------------
    if not row.empty:
        row = row.iloc[0]
        factor = grams / 100

        return {
            "calories": float(row["Calories (kcal)"]) * factor,
            "protein": float(row["Protein (g)"]) * factor,
            "carbohydrates": float(row["Carbohydrates (g)"]) * factor,
            "fat": float(row["Fat (g)"]) * factor,
            "fiber": float(row["Fiber (g)"]) * factor,
            "sugar": float(row["Sugars (g)"]) * factor,
            "sodium": float(row["Sodium (mg)"]) * factor
        }

    # -------------------------
    # CASE 2: UNKNOWN FOOD
    # -------------------------
    category = get_food_category(food)

    CATEGORY_AVG = {
        "Fruit": {
            "calories": 52, "protein": 0.3, "carbohydrates": 14,
            "fat": 0.2, "fiber": 2.4, "sugar": 10, "sodium": 1
        },
        "Vegetable": {
            "calories": 25, "protein": 2, "carbohydrates": 5,
            "fat": 0.1, "fiber": 3, "sugar": 2, "sodium": 20
        },
        "Grain": {
            "calories": 130, "protein": 3, "carbohydrates": 28,
            "fat": 0.4, "fiber": 2, "sugar": 0.5, "sodium": 1
        },
        "Default": {
            "calories": 100, "protein": 3, "carbohydrates": 15,
            "fat": 2, "fiber": 2, "sugar": 5, "sodium": 50
        }
    }

    base = CATEGORY_AVG.get(category, CATEGORY_AVG["Default"])
    factor = grams / 100

    return {
        "calories": base["calories"] * factor,
        "protein": base["protein"] * factor,
        "carbohydrates": base["carbohydrates"] * factor,
        "fat": base["fat"] * factor,
        "fiber": base["fiber"] * factor,
        "sugar": base["sugar"] * factor,
        "sodium": base["sodium"] * factor
    }


# =========================================================
# CATEGORY FUNCTION (SAFE VERSION)
# =========================================================

def get_food_category(food):
    food = food.strip().lower()
    row = df[df["Food_Item"].apply(lambda x: food in x)]

    if not row.empty:
        return row.iloc[0]["Category"]

    return "Default"