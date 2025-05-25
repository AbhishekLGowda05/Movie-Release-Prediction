import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
df = pd.read_csv("../data/cleaned_movies.csv")
print("✅ Data loaded:")
print(df.head())

# Convert release_date to datetime if not already
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

# Extract year
df["year"] = df["release_date"].dt.year

# Flatten genres into individual rows (for multi-genre movies)
# Explode genres: currently stored as string lists, need to convert to real lists first
import ast

# Convert string to list
df["genres"] = df["genres"].apply(lambda x: ast.literal_eval(x))

# Explode into separate rows per genre
exploded = df.explode("genres")


# Set visual style
sns.set(style="whitegrid")

# 1️⃣ Genre frequency
plt.figure(figsize=(10, 6))
genre_counts = exploded["genres"].value_counts()
sns.barplot(x=genre_counts.index, y=genre_counts.values)
plt.title("Most Common Movie Genres")
plt.ylabel("Number of Movies")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../assets/genre_frequency.png")
plt.show()

# 2️⃣ Rating distribution
plt.figure(figsize=(10, 6))
sns.histplot(df["vote_average"], bins=20, kde=True)
plt.title("Distribution of Average Ratings")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("../assets/rating_distribution.png")
plt.show()

# 3️⃣ Popularity trend over years
plt.figure(figsize=(10, 6))
yearly_popularity = df.groupby("year")["popularity"].mean()
sns.lineplot(x=yearly_popularity.index, y=yearly_popularity.values)
plt.title("Average Popularity Over Years")
plt.xlabel("Year")
plt.ylabel("Average Popularity")
plt.tight_layout()
plt.savefig("../assets/popularity_trend.png")
plt.show()

print("✅ EDA plots saved in ../assets/")
