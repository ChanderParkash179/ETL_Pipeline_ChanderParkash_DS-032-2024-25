# -*- coding: utf-8 -*-
"""etl_pipeline.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EZ6Jd_y-qmS4gxOrEvNLkkV5O2oaqtS2
"""

# Install packages from requirements.txt
!pip install -r requirements.txt

import requests
import pandas as pd
import kagglehub
from google.colab import files
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import faker
import json
import os
import openpyxl

try:
    result = subprocess.run(["python3", "./load_to_db.py"], check=True, capture_output=True, text=True)
    print("✅ Script executed successfully!\n")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("❌ Failed to run load_to_db.py")
    print("🔍 Error Output:\n", e.stderr)

# Function to extract data from CSV
def extract_csv(file_path):
    print(f"❯ Extracting CSV from {file_path}...")
    return pd.read_csv(file_path).to_dict(orient="records")

# Function to extract data from JSON
def extract_json(file_path):
    print(f"❯ Extracting JSON from {file_path}...")
    with open(file_path, "r") as f:
        return json.load(f)

# Function to extract data from Excel
def extract_excel(file_path):
    print(f"❯ Extracting Excel from {file_path}...")
    return pd.read_excel(file_path).to_dict(orient="records")

# Function to extract data from MongoDB collection
def extract_mongodb(mongo_uri, db_name, collection_name):
    print(f"❯ Extracting data from MongoDB...")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    return list(collection.find())

# Function to transform the data (e.g., cleaning or adding new fields)
def transform_data(data):
    print(f"❯ Transforming data...")

    # Remove duplicates based on Name & Country or Name & Sport
    seen_records = set()
    cleaned_data = []

    for record in data:
        name = record.get("Name", "").strip()
        country = record.get("Country", "").strip()
        sport = record.get("Sport", "").strip()

        # Create composite keys based on (Name & Country) or (Name & Sport)
        if (name, country) not in seen_records and (name, sport) not in seen_records:
            seen_records.add((name, country))
            seen_records.add((name, sport))
            cleaned_data.append(record)

    # Apply transformations like cleaning, unit conversions, etc.
    transformed_data = []
    for record in cleaned_data:
        # Data Cleaning: Handle missing values and erroneous values
        if 'Sport' not in record or not record['Sport']:
            record['Sport'] = 'Unknown'
        if 'Team' not in record or not record['Team']:
            record['Team'] = 'Unknown'

        transformed_data.append(record)

    return transformed_data

# Function to load data into MongoDB
def load_to_mongodb(mongo_uri, db_name, collection_name, data):
    print(f"❯ Loading data into MongoDB collection '{collection_name}'...")

    # Connect to MongoDB
    client = MongoClient(mongo_uri)

    # Access the database (MongoDB will create it if it doesn't exist)
    db = client[db_name]

    # Access the collection (MongoDB will create it if it doesn't exist)
    collection = db[collection_name]

    # Insert data into the collection
    result = collection.insert_many(data)

    # Print success message with the number of records inserted
    print(f"✅ Inserted {len(result.inserted_ids)} records into '{collection_name}' collection in '{db_name}' database.")

# Combine data from multiple sources (CSV, JSON, Excel, MongoDB)
def extract_data_from_files_and_mongo():
    # Example of reading from CSV, JSON, and Excel files (this should be adapted to your actual paths)
    csv_data = pd.read_csv("./data/sports_data.csv").to_dict(orient="records")
    json_data = json.load(open("./data/sports_data.json", "r"))
    excel_data = pd.read_excel("./data/sports_data.xlsx").to_dict(orient="records")
    mongo_data = list(collection.find())

    all_data = csv_data + json_data + excel_data + mongo_data
    return all_data

# Main ETL pipeline function
def etl_pipeline():
    # MongoDB connection URI and database name
    with open("./config/db_config.json", "r") as f:
        config = json.load(f)

    mongo_uri = config.get("mongo_uri")
    db_name = "sports_data"  # Change as needed
    collection_name = "sports_data"

    # Extract data from different sources
    csv_data = extract_csv("./data/sports_data.csv")
    json_data = extract_json("./data/sports_data.json")
    excel_data = extract_excel("./data/sports_data.xlsx")
    mongo_data = extract_mongodb(mongo_uri, db_name, collection_name)

    # Combine all data into one list
    all_data = csv_data + json_data + excel_data + mongo_data

    # Transform the data
    transformed_data = transform_data(all_data)

    # Load transformed data into MongoDB
    load_to_mongodb(mongo_uri, db_name, "load_sports_data", transformed_data)

    # total records was
    print(f"✅ Total records were {len(all_data)}")

# execute pipeline
if __name__ == "__main__":
    etl_pipeline()

# Method to query data from MongoDB and save it as CSV
def export_data_to_csv(mongo_uri, db_name, collection_name, output_dir='./output', csv_file_name='final_cleaned_data.csv'):
    print(f"❯ Querying data from MongoDB collection '{collection_name}' in database '{db_name}'...")

    # Establish connection to MongoDB
    data_from_db = extract_mongodb(mongo_uri, db_name, collection_name)

    # available data
    print(f'available loaded data: {len(data_from_db)}')

    # Convert data to DataFrame
    df = pd.DataFrame(list(data_from_db))

    # Ensure the 'output' folder exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Path to save the CSV file
    csv_file_path = os.path.join(output_dir, csv_file_name)

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

    print(f"✅ Data successfully saved to {csv_file_path}")

    # If you want to download the file from Colab to your local machine
    files.download(csv_file_path)

with open("./config/db_config.json", "r") as f:
  config = json.load(f)

  mongo_uri = config.get("mongo_uri")

# Call the method to export data from MongoDB collection to CSV
export_data_to_csv(mongo_uri, "sports_data", "load_sports_data")