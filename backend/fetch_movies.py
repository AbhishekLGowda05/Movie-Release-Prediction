import requests
import json
import os
from dotenv import load_dotenv

# Load the TMDb API key from .env
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# TMDb endpoint to get popular movies
BASE_URL = "https://api.themoviedb.org/3"
ENDPOINT = "/discover/movie"

# Define parameters for the request
params = {
    "api_key": API_KEY,
    "language": "en-US",
    "sort_by": "popularity.desc",
    "include_adult": "true",
    "include_video": "false",
    "page": 1,
    "primary_release_date.gte": "2010-01-01",  # From 2010 onwards
    "with_original_language": "en"             # English movies
}

# Create a list to store results
all_movies = []

# Loop through the first 5 pages
for page in range(1, 6):
    print(f"Fetching page {page}...")
    params["page"] = page
    response = requests.get(BASE_URL + ENDPOINT, params=params)

    if response.status_code == 200:
        data = response.json()
        for movie in data["results"]:
            movie_data = {
                "id": movie["id"],
                "title": movie["title"],
                "release_date": movie.get("release_date", ""),
                "genre_ids": movie.get("genre_ids", []),
                "popularity": movie.get("popularity", 0),
                "vote_average": movie.get("vote_average", 0),
                "vote_count": movie.get("vote_count", 0)
            }
            all_movies.append(movie_data)
    else:
        print(f"Failed to fetch page {page}. Status code: {response.status_code}")

# Save the results
output_path = "../data/popular_movies.json"
with open(output_path, "w") as f:
    json.dump(all_movies, f, indent=4)

print(f"✅ Successfully saved {len(all_movies)} movies to {output_path}")
