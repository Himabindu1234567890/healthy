from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import joblib
import json
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from n import analyze_food_health
print("RUNNING FILE:", __file__)

# -------------------------------
# CUSTOM UTILS
# -------------------------------
from food_utils import (
    get_food_list,
    calculate_grams,
    get_nutrients,
    get_food_category
)

from diet_engine.plan_generator import generate_daily_plan
from camera_module import camera_bp
# -------------------------------
# APP INIT
# -------------------------------
app = Flask(__name__)
app.secret_key = "nutrisense_secret_key"

app.register_blueprint(camera_bp)
def get_db_connection():
    conn = sqlite3.connect("nutrisense.db")
    conn.row_factory = sqlite3.Row
    return conn
conn = get_db_connection()

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()
conn.close()
# -------------------------------
# LOAD ML MODELS
# -------------------------------
model = joblib.load("model/nutrition_risk_model.pkl")
scaler = joblib.load("model/scaler.pkl")
encoder = joblib.load("model/label_encoder.pkl")

# -------------------------------
# LOAD JSON CONFIGS
# -------------------------------
with open("data/portion_mapping.json") as f:
    PORTION_MAP = json.load(f)
PORTION_MAP = {
    k.strip().lower(): {uk.strip().lower(): uv for uk, uv in v.items()}
    for k, v in PORTION_MAP.items()
}

with open("data/category_unit_map.json") as f:
    CATEGORY_UNIT_MAP = json.load(f)

# -------------------------------
# HYBRID RISK LOGIC
# -------------------------------
def hybrid_risk_prediction(ml_risk, features):
    calories, protein, carbs, fat, fiber, sugar, sodium, water = features

    if calories <= 250 and sugar <= 30 and fat <= 15 and sodium <= 500:
        return "Healthy"

    return ml_risk

# ======================================================
# HOME / NUTRITION INPUT PAGE (OLD MAIN PAGE)
# ======================================================
@app.route("/")
def nutrition_risk_page():
    foods = get_food_list()
    food_category_map = {f: get_food_category(f) for f in foods}

    return render_template(
        "index.html",
        foods=foods,
        portion_map=PORTION_MAP,
        category_unit_map=CATEGORY_UNIT_MAP,
        food_category_map=food_category_map
    )

# ======================================================
# PREDICT ROUTE
# ======================================================

@app.route("/predict", methods=["POST"])
def predict():
    final_risk = "Healthy"

    # ---------- INPUT ----------
    foods_dropdown = request.form.getlist("food[]")
    foods_custom = request.form.getlist("food_custom[]")
    units = request.form.getlist("unit[]")
    counts = request.form.getlist("count[]")

    foods = []
    for drop, custom in zip(foods_dropdown, foods_custom):
        foods.append(custom.strip() if custom else drop)

    # ---------- WATER ----------
    water = request.form.get("water_intake")
    water = float(water) if water not in [None, ""] else 0.0

    # ---------- TOTAL ----------
    total = {
        "calories": 0.0,
        "protein": 0.0,
        "carbohydrates": 0.0,
        "fat": 0.0,
        "fiber": 0.0,
        "sugar": 0.0,
        "sodium": 0.0
    }

    # ---------- LOOP ----------
    for f, u, c in zip(foods, units, counts):
        if not f or not u or not c:
            continue

        grams = calculate_grams(f, u, c)

        print("👉 Food:", f)
        print("👉 Unit:", u)
        print("👉 Count:", c)
        print("👉 Grams:", grams)
        nutrients = get_nutrients(f, grams)
        print("Nutrients:", nutrients)

        for k in total:
            total[k] += nutrients.get(k, 0)

    # ✅ AFTER LOOP ONLY
    print("FINAL TOTAL:", total)

    total = {k: float(v) for k, v in total.items()}

    # ---------- RISK ----------
    from n import get_food_risk_from_dataset

    risks = []
    for f in foods:
        r = get_food_risk_from_dataset(f)
        if r:
            risks.append(r)

    if "Unhealthy" in risks:
        final_risk = "Unhealthy"
    elif "Moderate" in risks:
        final_risk = "Moderate"

    print("FINAL RISK:", final_risk)

    # ---------- BMI ----------
    height = request.form.get("height")
    weight = request.form.get("weight")

    bmi = None
    bmi_status = None

    if height and weight:
        h = float(height) / 100
        bmi = round(float(weight) / (h * h), 2)

        if bmi < 18.5:
            bmi_status = "Underweight"
        elif bmi < 25:
            bmi_status = "Normal"
        elif bmi < 30:
            bmi_status = "Overweight"
        else:
            bmi_status = "Obese"

    # ✅ SAVE SESSION (ONLY HERE)
    session["dashboard_data"] = {
        "risk": final_risk,
        "nutrients": total,
        "water": water,
        "bmi": bmi,
        "bmi_status": bmi_status
    }

    return redirect(url_for("dashboard"))
@app.route("/auth")
def auth():
    return render_template("auth.html")
    

# ================================
# LOGIN ROUTE
# ================================
# ================================
# LOGIN PAGE (GET)
# ================================
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


# ================================
# SIGNUP PAGE (GET)
# ================================
@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")
@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    ).fetchone()

    conn.close()

    if user:
        session["user"] = user["name"]
        return redirect("/dashboard")

    return "Invalid email or password"


# ================================
# SIGNUP ROUTE
# ================================
@app.route("/signup", methods=["POST"])
def signup():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    conn = get_db_connection()

    # Check if email already exists
    existing_user = conn.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    ).fetchone()

    if existing_user:
        conn.close()
        return "User already exists"

    conn.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, password)
    )

    conn.commit()
    conn.close()

    session["user"] = name

    return redirect("/dashboard")


# ================================
# LOGOUT ROUTE
# ================================
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")

# ======================================================
# DASHBOARD PAGE
# ======================================================
@app.route("/dashboard")
def dashboard():
    data = session.get("dashboard_data", {})
    profile = session.get("profile", {})

    return render_template(
        "dashboard.html",
        risk=data.get("risk"),
        nutrients=data.get("nutrients", {}),
        water=data.get("water", 0),
        bmi=data.get("bmi"),
        bmi_status=data.get("bmi_status"),
        profile=profile

    )
    
# ======================================================
# PROFILE PAGE
# ======================================================
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        session["profile"] = {
            "name": request.form.get("name"),
            "age": request.form.get("age"),
            "gender": request.form.get("gender"),
            "height": request.form.get("height"),
            "weight": request.form.get("weight"),
            "disease": request.form.get("disease")
        }
        return redirect(url_for("dashboard"))

    return render_template(
        "profile.html",
        profile=session.get("profile", {})
    )

# ======================================================
# DIET PLAN PAGE
# ======================================================
@app.route("/diet-plan", methods=["GET", "POST"])
def diet_plan_page():
    plan = None
    disease = None
    age = None

    if request.method == "POST":
        disease = request.form.get("disease")
        age = request.form.get("age")

        smoker = request.form.get("smoker") == "yes"
        drinker = request.form.get("drinker") == "yes"

        if disease and age:
            age = int(age)
            plan = generate_daily_plan(
                disease,
                age,
                smoker=smoker,
                drinker=drinker
            )

    return render_template(
        "diet_plan.html",
        plan=plan,
        disease=disease,
        age=age
    )



# ======================================================
# MEAL DETAIL PAGE
# ======================================================
@app.route("/meal-plan/<meal>")
def meal_plan_detail(meal):
    disease = request.args.get("disease", "None")

    meal_data = {

        # ======================
        # 🍳 BREAKFAST
        # ======================
        "breakfast": {
            "Diabetes": {
                "time": "8:00 AM",
                "foods": [
                    "Oats", "Apple", "Papaya",
                    "Milk", "Boiled Egg", "Sprouts"
                ],
                "avoid": [
                    "White Bread", "Jam", "Sugar",
                    "Cornflakes", "Pancakes", "Sweet Juice"
                ],
                "reason": "Low GI foods help control blood sugar levels"
            },

            "None": {
                "time": "8:00 AM",
                "foods": [
                    "Idli", "Milk", "Banana",
                    "Apple", "Egg", "Sprouts"
                ],
                "avoid": [
                    "Deep Fried Snacks", "Sugary Drinks",
                    "Pastries", "Chocolates", "Chips", "Cola"
                ],
                "reason": "Balanced breakfast provides energy for the day"
            }
        },

        # ======================
        # 🍛 LUNCH
        # ======================
        "lunch": {
            "Diabetes": {
                "time": "1:00 PM",
                "foods": [
                    "Chapati", "Brown Rice", "Vegetables",
                    "Dal", "Salad", "Curd"
                ],
                "avoid": [
                    "White Rice", "Fried Rice",
                    "Potato Curry", "Pickles",
                    "Soft Drinks", "Sweets"
                ],
                "reason": "Fiber-rich meals prevent glucose spikes"
            },

            "None": {
                "time": "1:00 PM",
                "foods": [
                    "Rice", "Dal", "Vegetables",
                    "Curd", "Salad", "Chapati"
                ],
                "avoid": [
                    "Excess Oil", "Fast Food",
                    "Sugary Drinks", "Overeating",
                    "Fried Items", "Too Much Salt"
                ],
                "reason": "Balanced nutrients support digestion and energy"
            }
        },

        # ======================
        # ☕ SNACK
        # ======================
        "snack": {
            "Diabetes": {
                "time": "5:00 PM",
                "foods": [
                    "Nuts", "Green Tea", "Roasted Chana",
                    "Apple", "Buttermilk", "Sprouts"
                ],
                "avoid": [
                    "Biscuits", "Cakes", "Soft Drinks",
                    "Samosa", "Puffs", "Sweet Tea"
                ],
                "reason": "Healthy snacks avoid sugar spikes"
            },

            "None": {
                "time": "5:00 PM",
                "foods": [
                    "Nuts", "Tea", "Fruits",
                    "Corn", "Milk", "Roasted Chana"
                ],
                "avoid": [
                    "Chips", "Cola", "Puffs",
                    "Pastries", "Cream Biscuits", "Fried Snacks"
                ],
                "reason": "Light snacks maintain energy levels"
            }
        },

        # ======================
        # 🌙 DINNER
        # ======================
        "dinner": {
            "Diabetes": {
                "time": "8:00 PM",
                "foods": [
                    "Chapati", "Soup", "Vegetables",
                    "Dal", "Salad", "Curd"
                ],
                "avoid": [
                    "White Rice", "Fried Foods",
                    "Sweets", "Late Night Snacks",
                    "Soft Drinks", "Heavy Meals"
                ],
                "reason": "Light dinner supports sugar control and digestion"
            },

            "None": {
                "time": "8:00 PM",
                "foods": [
                    "Roti", "Vegetables", "Soup",
                    "Dal", "Curd", "Salad"
                ],
                "avoid": [
                    "Heavy Rice", "Fast Food",
                    "Late Eating", "Sugary Desserts",
                    "Oily Foods", "Cold Drinks"
                ],
                "reason": "Light meals improve sleep and digestion"
            }
        }
    }

    # fallback if disease not found
    details = meal_data.get(meal, {}).get(disease) \
              or meal_data.get(meal, {}).get("None")

    return render_template(
        "meal_detail.html",
        meal=meal.capitalize(),
        disease=disease,
        details=details
    )
@app.route("/foodchat", methods=["POST"])
def food_chat():

    user_message = request.json["message"].lower()

    food_data = {
        "apple": {"calories": 52, "diabetes": "Apple is good for diabetes in moderate amounts."},
        "banana": {"calories": 89, "diabetes": "Banana should be eaten in small quantities for diabetes."},
        "rice": {"calories": 130, "diabetes": "White rice may increase blood sugar levels."},
        "egg": {"calories": 155, "diabetes": "Egg is healthy and good for protein."},
        "milk": {"calories": 42, "diabetes": "Milk is generally safe but should be consumed moderately."},
        "chicken": {"calories": 239, "diabetes": "Chicken is a good protein food and generally healthy."}
    }

    for food in food_data:

        if food in user_message:

            if "calorie" in user_message:
                return jsonify({"response": f"{food} contains about {food_data[food]['calories']} calories per 100g."})

            if "sugar" in user_message or "diabetes" in user_message:
                return jsonify({"response": food_data[food]["diabetes"]})

            if "healthy" in user_message:
                return jsonify({"response": f"Yes, {food} is generally considered healthy when eaten in moderation."})

            return jsonify({"response": f"{food} has about {food_data[food]['calories']} calories per 100g and can be part of a healthy diet."})

    # General keyword answers
    if "diet" in user_message:
        return jsonify({"response": "A balanced diet includes proteins, carbohydrates, healthy fats, fruits and vegetables."})

    if "water" in user_message:
        return jsonify({"response": "Adults should drink around 2-3 liters of water per day."})

    return jsonify({"response": "Please ask about foods like apple, banana, egg, rice, milk, chicken etc."})



# ======================================================
# STATIC PAGES
# ======================================================
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/home")
def home():
    return render_template("home.html")
from flask import request, jsonify

@app.route("/receive-food", methods=["POST"])
def receive_food():
    data = request.json
    print("Received food:", data)

    return jsonify({"status": "ok"})


# ======================================================
# RUN APP
# ======================================================
if __name__ == "__main__":
    app.run(debug=True, port=5001)