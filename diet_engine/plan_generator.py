# -----------------------------
# AGE GROUP LOGIC
# -----------------------------
def get_age_group(age):
    if age < 18:
        return "child"
    elif age <= 40:
        return "adult"
    elif age <= 60:
        return "middle"
    else:
        return "senior"


# -----------------------------
# APPLY LIFESTYLE MODIFICATIONS
# -----------------------------
def apply_lifestyle_modifications(plan, smoker=False, drinker=False):
    if not plan:
        return plan

    # =========================
    # SMOKER (HIGH PRIORITY)
    # =========================
    if smoker:
        # REMOVE harmful foods first
        for meal in ["Breakfast", "Lunch", "Dinner"]:
            plan[meal]["diet"] = [
                f for f in plan[meal]["diet"]
                if f not in ["Fried Foods", "Bakery Items", "Processed Foods"]
            ]

        # FORCE ADD antioxidant foods
        plan["Breakfast"]["diet"] = [
            "Lemon Water", "Orange", "Guava"
        ] + plan["Breakfast"]["diet"]

        # MODIFY snacks
        plan["Evening Snack"]["diet"] = ["Green Tea", "Fruits"]

        # STRONG avoid list
        plan["Avoid"] = list(set(
            plan["Avoid"] + ["Cigarettes", "Caffeine", "Processed Foods"]
        ))

        plan["Lifestyle"]["Smoking Note"] = (
            "Antioxidant-rich foods added to reduce smoking impact"
        )

    # =========================
    # DRINKER (HIGH PRIORITY)
    # =========================
    if drinker:
        # FORCE light dinner (OVERRIDE)
        plan["Dinner"]["diet"] = ["Soup", "Vegetables", "Buttermilk"]

        # HYDRATION focus
        plan["Lifestyle"]["Drinking Note"] = (
            "Liver-friendly and hydration-focused diet applied"
        )

        plan["Avoid"] = list(set(
            plan["Avoid"] + ["Alcohol", "Sugary Mixers", "Late-night Snacks"]
        ))

    return plan



# -----------------------------
# MAIN PLAN GENERATOR
# -----------------------------
def generate_daily_plan(disease, age, smoker=False, drinker=False):
    age_group = get_age_group(age)

    # =============================
    # NORMAL DIET
    # =============================
    if disease == "None" or not disease:

        plan = {
            "Breakfast": {
                "time": "8:00 AM",
                "diet": ["Idli", "Milk", "Fruits", "Egg", "Vegetables", "Curd", "Banana"]
            },
            "Lunch": {
                "time": "1:00 PM",
                "diet": ["Rice", "Dal", "Vegetables", "Curd", "Salad", "Chapati", "Soup"]
            },
            "Evening Snack": {
                "time": "5:00 PM",
                "diet": ["Nuts", "Green Tea", "Fruits"]
            },
            "Dinner": {
                "time": "8:00 PM",
                "diet": ["Chapati", "Vegetables", "Soup"]
            },
            "Lifestyle": {
                "Exercise": "30 minutes walking",
                "Water": "8 glasses",
                "Sleep": "7–8 hours"
            },
            "Avoid": ["Overeating", "Late-night snacks"]
        }

        return apply_lifestyle_modifications(plan, smoker, drinker)

    # =============================
    # DIABETES
    # =============================
    if disease == "Diabetes":

        plan = {
            "Breakfast": {
                "time": "8:00 AM",
                "diet": ["Oats", "Apple", "Milk", "Nuts", "Boiled Egg", "Vegetables", "Curd"]
            },
            "Lunch": {
                "time": "1:00 PM",
                "diet": ["Chapati", "Brown Rice", "Vegetables", "Dal", "Salad", "Soup"]
            },
            "Evening Snack": {
                "time": "5:00 PM",
                "diet": ["Green Tea", "Roasted Chana", "Nuts"]
            },
            "Dinner": {
                "time": "8:00 PM",
                "diet": ["Chapati", "Vegetables", "Soup"]
            },
            "Lifestyle": {
                "Exercise": "30 minutes brisk walking",
                "Water": "8–10 glasses",
                "Sleep": "7–8 hours"
            },
            "Avoid": [
                "White Rice",
                "Sugar",
                "Sweets",
                "Soft Drinks",
                "White Bread",
                "Fried Foods",
                "Bakery Items"
            ]
        }

        return apply_lifestyle_modifications(plan, smoker, drinker)

    # =============================
    # HYPERTENSION
    # =============================
    if disease == "Hypertension":

        plan = {
            "Breakfast": {
                "time": "8:00 AM",
                "diet": ["Oats", "Banana", "Milk", "Fruits", "Curd", "Boiled Egg"]
            },
            "Lunch": {
                "time": "1:00 PM",
                "diet": ["Rice", "Low-salt Dal", "Vegetables", "Salad", "Soup"]
            },
            "Evening Snack": {
                "time": "5:00 PM",
                "diet": ["Green Tea", "Fruits", "Nuts"]
            },
            "Dinner": {
                "time": "8:00 PM",
                "diet": ["Chapati", "Vegetables", "Soup"]
            },
            "Lifestyle": {
                "Exercise": "Yoga / breathing exercises",
                "Water": "8 glasses",
                "Sleep": "7–8 hours"
            },
            "Avoid": [
                "Salt",
                "Pickles",
                "Fried Foods",
                "Processed Foods",
                "Fast Food",
                "Papad",
                "Chips"
            ]
        }

        return apply_lifestyle_modifications(plan, smoker, drinker)

    # =============================
    # OBESITY
    # =============================
    if disease == "Obesity":

        plan = {
            "Breakfast": {
                "time": "8:00 AM",
                "diet": ["Oats", "Apple", "Fruits", "Boiled Egg", "Vegetables"]
            },
            "Lunch": {
                "time": "1:00 PM",
                "diet": ["Millets", "Vegetables", "Dal", "Salad", "Soup"]
            },
            "Evening Snack": {
                "time": "5:00 PM",
                "diet": ["Green Tea", "Fruits"]
            },
            "Dinner": {
                "time": "8:00 PM",
                "diet": ["Soup", "Vegetables"]
            },
            "Lifestyle": {
                "Exercise": "45 minutes cardio",
                "Water": "10–12 glasses",
                "Sleep": "7–9 hours"
            },
            "Avoid": [
                "Fast Food",
                "Sugary Snacks",
                "Fried Foods",
                "Bakery Items",
                "Soft Drinks",
                "Ice Cream",
                "Chips"
            ]
        }

        return apply_lifestyle_modifications(plan, smoker, drinker)

    return None
