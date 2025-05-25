import pandas as pd
import ast

# Load cleaned data
df = pd.read_csv("../data/cleaned_movies.csv")

# Convert genres string back to list
df["genres"] = df["genres"].apply(lambda x: ast.literal_eval(x))

# Extract year, month, and derive season
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

# One-hot encode season
season_dummies = pd.get_dummies(df["season"], prefix="season")

# Multi-hot encode genres
all_genres = ["Action", "Comedy", "Drama", "Romance", "Horror", "Thriller", "Other"]
for genre in all_genres:
    df[f"genre_{genre}"] = df["genres"].apply(lambda x: int(genre in x))

# Combine features
feature_cols = ["popularity", "vote_average", "vote_count"] + list(season_dummies.columns) + [f"genre_{g}" for g in all_genres]
X = pd.concat([df[["popularity", "vote_average", "vote_count"]], season_dummies, df[[f"genre_{g}" for g in all_genres]]], axis=1)

# Define label: best release season
y = df["season"]

# Save features and labels
X.to_csv("../data/features_X.csv", index=False)
y.to_csv("../data/labels_y.csv", index=False)

print(f"✅ Features saved to ../data/features_X.csv")
print(f"✅ Labels saved to ../data/labels_y.csv")
print(f"✅ Feature shape: {X.shape}, Label shape: {y.shape}")
