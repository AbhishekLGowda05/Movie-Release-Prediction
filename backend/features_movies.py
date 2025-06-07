import pandas as pd
import ast

# Load cleaned data
df = pd.read_csv("../data/cleaned_movies_corrected.csv")

# ✅ Add dummy rows BEFORE encoding
dummy_rows = pd.DataFrame({
    "genres": ["['Other']"] * 12,  # Must be a string, not a list!
    "platform": ["Cinema", "OTT", "Both"] * 4,
    "region": ["India", "USA", "Europe", "Global"] * 3,
    "release_date": pd.to_datetime(["2024-01-01"] * 12)
})

df = pd.concat([df, dummy_rows], ignore_index=True)

# ✅ Convert genre string to actual list
df["genres"] = df["genres"].apply(lambda x: ast.literal_eval(x))

# Extract year, month, and derive season (used as the label)
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df["year"] = df["release_date"].dt.year
df["month"] = df["release_date"].dt.month

def assign_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

df["season"] = df["month"].apply(assign_season)

# ✅ Multi-hot encode genres
all_genres = ["Action", "Comedy", "Drama", "Romance", "Horror", "Thriller", "Other"]
for genre in all_genres:
    df[f"genre_{genre}"] = df["genres"].apply(lambda x: int(genre in x))

# ✅ One-hot encode platform and region
platform_dummies = pd.get_dummies(df["platform"], prefix="platform")
region_dummies = pd.get_dummies(df["region"], prefix="region")

# ✅ Combine all features
X = pd.concat([platform_dummies, region_dummies, df[[f"genre_{g}" for g in all_genres]]], axis=1)

# ✅ Define label
y = df["season"]

# ✅ Save features and labels
X.to_csv("../data/features_X_corrected.csv", index=False)
y.to_csv("../data/labels_y_corrected.csv", index=False)

print(f"✅ Corrected features saved to ../data/features_X_corrected.csv")
print(f"✅ Corrected labels saved to ../data/labels_y_corrected.csv")
print(f"✅ Feature shape: {X.shape}, Label shape: {y.shape}")
