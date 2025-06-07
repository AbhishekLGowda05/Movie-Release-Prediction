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

# Map genre IDs to names (hardcoded mapping)
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

# Add placeholders for platform and region (since TMDb doesn't provide these directly)
df["platform"] = "Cinema"   # Options: Cinema, OTT, Both
df["region"] = "India"      # Options: India, USA, Europe, Global

# Select only necessary columns
df_cleaned = df[["id", "title", "release_date", "genres", "platform", "region"]]

print("\n✅ Cleaned data preview:")
print(df_cleaned.head())

# Save to CSV
output_path = "../data/cleaned_movies_corrected.csv"
df_cleaned.to_csv(output_path, index=False)

print(f"\n✅ Corrected cleaned data saved to {output_path}")
