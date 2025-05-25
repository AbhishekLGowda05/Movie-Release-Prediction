import pandas as pd
import json

# Load raw JSON data
with open("../data/popular_movies.json", "r") as f:
    raw_data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(raw_data)

print("✅ Loaded raw data:")
print(df.head())

# Check for missing values
print("\n🔍 Checking for missing values:")
print(df.isnull().sum())

# Fill missing release dates with placeholder (if needed)
df["release_date"] = df["release_date"].replace("", "1900-01-01")
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

# Map genre IDs to names (we’ll hardcode a basic mapping for now)
genre_map = {
    28: "Action",
    35: "Comedy",
    18: "Drama",
    10749: "Romance",
    27: "Horror",
    53: "Thriller"
}

# Convert genre IDs list → genre names list
def map_genres(genre_ids):
    return [genre_map.get(gid, "Other") for gid in genre_ids]

df["genres"] = df["genre_ids"].apply(map_genres)

# Drop unnecessary columns
df_cleaned = df[["id", "title", "release_date", "genres", "popularity", "vote_average", "vote_count"]]

print("\n✅ Cleaned data preview:")
print(df_cleaned.head())

# Save to CSV
output_path = "../data/cleaned_movies.csv"
df_cleaned.to_csv(output_path, index=False)

print(f"\n✅ Cleaned data saved to {output_path}")
