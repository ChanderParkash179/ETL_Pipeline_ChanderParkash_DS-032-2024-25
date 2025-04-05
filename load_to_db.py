import json
from pymongo import MongoClient

# Step 1: Load config
with open("/content/db_config.json", "r") as f:
    config = json.load(f)

mongo_uri = config.get("mongo_uri")
if not mongo_uri:
    raise ValueError("❌ 'mongo_uri' not found in db_config.json")

try:
    # Step 2: Connect to MongoDB
    client = MongoClient(mongo_uri)

    # Use database and collection
    db = client["sports_data"]
    collection = db["sports_data"]

    # Confirm connection
    print("✅ Connected to MongoDB!")
    print(f"📂 Database: sports_data, Collection: sports_data")
    print(f"🔢 Existing Documents: {collection.count_documents({})}")

    # Step 3: Load data and insert into MongoDB
    with open("/content/mongo_records.json", "r") as f:
        records = json.load(f)

    result = collection.insert_many(records)
    print(f"✅ Inserted {len(result.inserted_ids)} new records into 'sports_data' collection.")

except Exception as e:
    print("❌ Failed to connect or insert into MongoDB.")
    print("🔍 Error:", e)
