from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Load the trained model
model = joblib.load("../data/release_season_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    
    try:
        # Extract features from request
        features = pd.DataFrame([data])
        
        # Predict
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features).max()
        
        response = {
            "predicted_season": prediction,
            "confidence": f"{probability:.2f}"
        }
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
