import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib

# ✅ correct path
df = pd.read_csv("data/final_nutrition_dataset_balanced.csv")

le = LabelEncoder()
le.fit(df['nutrition_risk'])

print("Classes:", le.classes_)

# ✅ overwrite correct file
joblib.dump(le, "model/label_encoder.pkl")

print("✅ label_encoder.pkl updated successfully!")