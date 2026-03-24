# 🥗 NutriSense – AI Based Nutrition Risk Prediction System

NutriSense is a full-stack AI-powered web application that analyzes food intake, predicts nutrition risk levels, and provides personalized diet plans based on disease conditions and age.

It combines Machine Learning, Flask, and an interactive dashboard to help users understand whether their diet is **Healthy, Moderate, or Unhealthy**.

---

## 🚀 Live Features

- 🔍 Nutrition Risk Prediction (Healthy / Moderate / Unhealthy)
- 📊 Interactive Real-Time Dashboard
- ⚖ BMI Calculation & Health Status
- 🍽 Disease-Based Personalized Diet Plan
- 👤 User Profile Management
- 📷 Live Food Detection using Camera (OpenCV)
- 📈 Nutrient Visualization Charts
- 🧠 Hybrid ML + Rule-Based System
- 🥗 Meal-wise Diet Plan with Food Images
- 💧 Water Intake Recommendation System
- 🔐 User Authentication (Login / Signup)
- 💬 AI Nutrition Chatbot for Food & Diet Queries

## 🧠 Machine Learning Details

- Dataset Size: 19,626 rows (Balanced)
- Final Cleaned Columns: 16 features
- Target Variable: `nutrition_risk`
- Classes: Healthy, Moderate, Unhealthy
- Models Compared:
  - Logistic Regression
  - Decision Tree
  - Random Forest ✅ (Selected Best Model)

Random Forest was selected based on:
- Highest Accuracy
- Better Generalization
- Stable Class Predictions

---

## 🏗 Tech Stack

### Backend
- Python
- Flask
- Scikit-learn
- Pandas
- NumPy

### Frontend
- HTML
- CSS
- JavaScript
- Chart.js

### ML Tools
- StandardScaler
- LabelEncoder
- RandomForestClassifier


### Other
- OpenCV (Live Camera Detection)
- Joblib (Model Saving)
- SQLite (User Authentication Database)

---

## 📊 Features Workflow

1. User selects or types food items
2. Nutrients are calculated dynamically
3. ML model predicts risk level
4. Hybrid logic adjusts risk if necessary
5. Dashboard updates automatically
6. Personalized diet plan generated
7. User can track BMI & health insights
8. Users can view recommended daily water intake
9. Users can login/signup to manage their profile
10. Users can ask food and nutrition questions using the chatbot

---


---

## 📈 Model Performance

- Accuracy: ~99% (Balanced Dataset)
- Balanced Classes
- No data leakage
- Clean feature scaling applied
- Consistent feature naming used

---

## 🔮 Future Improvements

- Cloud Deployment (Render / Railway)
- Downloadable Health Report (PDF)
- Weekly Trend Tracking
- Real-time Calorie Tracker
- API Integration for Food Database

---

## 👩‍💻 Author

**Team UNI 5** 
B.Tech – Computer Science (Data Science)  
Sri Venkateswara College of Engineering & Technology  

Passionate about AI, Machine Learning, and Full Stack Development.

---

## 💡 How to Run Locally

1. Clone the repository
2. Install dependencies:

