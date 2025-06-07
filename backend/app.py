import pandas as pd
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 
model = joblib.load("../data/release_season_model_corrected.pkl")

# Load expected column order from training file
expected_columns = pd.read_csv("../data/features_X_corrected.csv", nrows=1).columns.tolist()

genres = ["Action", "Comedy", "Drama", "Romance", "Horror", "Thriller", "Other"]
platforms = ["Cinema", "OTT", "Both"]
regions = ["India", "USA", "Europe", "Global"]

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        genre_input = data["genre"]
        platform_input = data["platform"]
        region_input = data["region"]

        # Construct full feature dict with 0s
        feature_dict = {col: 0 for col in expected_columns}

        # Set selected values to 1
        feature_dict[f"genre_{genre_input}"] = 1
        feature_dict[f"platform_{platform_input}"] = 1
        feature_dict[f"region_{region_input}"] = 1

        # Convert to DataFrame in the correct order
        input_df = pd.DataFrame([feature_dict])[expected_columns]

        # Predict
        prediction = model.predict(input_df)[0]
        confidence_scores = model.predict_proba(input_df)[0]
        classes = model.classes_
        confidence_map = {cls: round(score * 100, 2) for cls, score in zip(classes, confidence_scores)}

        return jsonify({
            "predicted_season": prediction,
            "confidence_scores": confidence_map
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
