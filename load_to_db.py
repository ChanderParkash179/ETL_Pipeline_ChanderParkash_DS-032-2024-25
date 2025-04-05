import json
import random
from faker import Faker
from pymongo import MongoClient

fake = Faker()

# Step 1: Load config
with open("/content/db_config.json", "r") as f:
    config = json.load(f)

mongo_uri = config.get("mongo_uri")
if not mongo_uri:
    raise ValueError("❌ 'mongo_uri' not found in db_config.json")

try:
    # Step 2: Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client["sports_data"]
    collection = db["sports_data"]

    print("✅ Connected to MongoDB!")
    print(f"📂 Database: sports_data, Collection: sports_data")
    print(f"🔢 Existing Documents: {collection.count_documents({})}")

    # Step 3: Generate 1000 random records from ID 1000+
    def generate_record(record_id):
        return {
            "ID": record_id,
            "Name": fake.name(),
            "Team": random.choice(['Lions', 'Tigers', 'Warriors', 'Knights', 'Eagles', 'Sharks']),
            "Sport": random.choice(['Football', 'Basketball', 'Cricket', 'Hockey']),
            "Nationality": random.choice(['USA', 'India', 'UK', 'Brazil', 'Germany', 'Australia'])
        }

    # Generate 1000 unique records first
    unique_records = [generate_record(1000 + i) for i in range(1000)]

    # Step 4: Create 400 duplicate records (40%)
    duplicates = random.sample(unique_records, 400)  # Choose 400 records to duplicate
    duplicate_records = []
    for record in duplicates:
        # Make sure the duplicated record doesn't have the same _id
        record_copy = record.copy()  # Make a copy of the record
        record_copy.pop('_id', None)  # Remove the _id field if it exists
        duplicate_records.append(record_copy)

    # Combine unique records and duplicates
    all_records = unique_records + duplicate_records

    # Step 5: Insert into MongoDB
    result = collection.insert_many(all_records)
    print(f"✅ Inserted {len(result.inserted_ids)} records into 'sports_data' collection (1000 records with 400 duplicates).")

except Exception as e:
    print("❌ Failed to connect or insert into MongoDB.")
    print("🔍 Error:", e)