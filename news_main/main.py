import requests
import pymongo
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["news_db"]
collection = db["articles"]

# Fetch data from News API
url = "https://newsapi.org/v2/top-headlines"
params = {
    "country": "us",
    "apiKey": API_KEY
}
response = requests.get(url, params=params)
data = response.json()

# Insert articles into MongoDB
if "articles" in data:
    collection.insert_many(data["articles"])
    print(f"Inserted {len(data['articles'])} articles.")
else:
    print("No articles found or error:", data)
