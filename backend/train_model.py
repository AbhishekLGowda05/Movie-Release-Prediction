import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load corrected features and labels
X = pd.read_csv("../data/features_X_corrected.csv")
y = pd.read_csv("../data/labels_y_corrected.csv").squeeze()

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n✅ Classification Report:")
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, "../data/release_season_model_corrected.pkl")
print("\n✅ Model saved as ../data/release_season_model_corrected.pkl")
