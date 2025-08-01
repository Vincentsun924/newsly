from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
from dotenv import load_dotenv
from typing import Optional
import os
import json

load_dotenv()

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["news_db"]
collection = db["articles"]

# Utility to convert ObjectId to string
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.get("/articles")
def get_articles():
    articles = list(collection.find().limit(20))
    return [serialize_doc(article) for article in articles]

@app.post("/articles")
def add_article(article: dict):
    result = collection.insert_one(article)
    return {"inserted_id": str(result.inserted_id)}

@app.delete("/articles/{article_id}")
def delete_article(article_id: str):
    result = collection.delete_one({"_id": ObjectId(article_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Deleted successfully"}


@app.put("/articles/{article_id}")
def update_article(article_id: str, update_fields: dict):
    try:
        result = collection.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": update_fields}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Article not found")

    return {"message": "Article updated successfully"}