# ETL Pipeline for Sports Data

## Chander Parkash
## Roll NO: DS-032/2024-25

## Overview
This project implements an ETL (Extract, Transform, Load) pipeline to process sports-related data from multiple sources and store it in a MongoDB database. The pipeline handles data from CSV, JSON, Excel files, and MongoDB collections, performs data cleaning and transformation, and finally exports the processed data to a CSV file.

## Features

- **Multi-source data extraction**: Supports CSV, JSON, Excel, and MongoDB sources
- **Data transformation**: 
  - Deduplication based on Name & Country or Name & Sport
  - Handling missing values (replacing empty fields with 'Unknown')
- **MongoDB integration**: 
  - Stores processed data in MongoDB collections
  - Retrieves data for analysis
- **Export functionality**: Converts final data to CSV for easy sharing and analysis

## Technical Stack

- Python 3
- MongoDB
- Key Python Packages:
  - pandas
  - pymongo
  - requests
  - matplotlib
  - seaborn
  - faker (for test data generation)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ChanderParkash179/ETL_Pipeline_ChanderParkash_DS-032-2024-25
   cd etl-pipeline
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up MongoDB:
   - Ensure MongoDB is running locally or configure a remote connection in `db_config.json`

## Usage

1. **Run the ETL pipeline**:
   ```python
   python etl_pipeline.ipynb
   ```

2. **Data flow**:
   - Extracts data from:
     - `/content/sports_data.csv`
     - `/content/sports_data.json`
     - `/content/sports_data.xlsx`
     - MongoDB `sports_data.sports_data` collection
   - Transforms the data (cleaning and deduplication)
   - Loads to MongoDB `sports_data.load_sports_data` collection
   - Exports final data to CSV at `/output/final_cleaned_data.csv`

## Sample Output

The pipeline will display progress messages:
```
❯ Extracting CSV from /content/sports_data.csv...
❯ Extracting JSON from /content/sports_data.json...
❯ Extracting Excel from /content/sports_data.xlsx...
❯ Extracting data from MongoDB...
❯ Transforming data...
❯ Loading data into MongoDB collection 'load_sports_data'...
✅ Inserted 1287 records into 'load_sports_data' collection in 'sports_data' database.
✅ Total records were 1700
```

## Data Structure

The processed data contains fields like:
- Name
- Nationality
- Sport
- Team

## Configuration

Modify `db_config.json` to specify your MongoDB connection URI:
```json
{
  "mongo_uri": "mongodb+srv://root:root@mid-term-cluster.mxl0ovi.mongodb.net/"
}
```

## Output

The final cleaned data is saved as:
- MongoDB collection: `sports_data.load_sports_data`
- CSV file: `/output/final_cleaned_data.csv`

## Performance

- Handles duplicate records efficiently
- Processes 1700 records in the sample dataset
- Outputs 1287 cleaned records after deduplication

## Scheduler

- it'll read from scheduler.py and run script after every 24 hours

## CI/CD Pipeline

- available cicd.yml file in .github/workflows/ path