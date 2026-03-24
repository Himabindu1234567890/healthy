# nutrition_patch.py
# Patch layer to correct nutrition risk output
# Does NOT modify existing application

def calculate_nutrition_status(data):
    """
    data = dictionary coming from your form
    example:
    {
        "calories": 500,
        "protein": 10,
        "fat": 20,
        "sugar": 30
    }
    """

    calories = float(data.get("calories", 0))
    protein = float(data.get("protein", 0))
    fat = float(data.get("fat", 0))
    sugar = float(data.get("sugar", 0))

    score = 0

    # scoring system
    if calories > 600:
        score += 1
    if sugar > 25:
        score += 1
    if fat > 20:
        score += 1
    if protein < 5:
        score += 1

    if score >= 3:
        return "High Risk"
    elif score == 2:
        return "Moderate Risk"
    else:
        return "Healthy"


def patch_dashboard_output(user_input, original_output):
    """
    Override incorrect output
    """

    corrected_status = calculate_nutrition_status(user_input)

    return {
        "status": corrected_status,
        "original_status": original_output
    }