import subprocess
import sys
import os

def run_etl_pipeline():
    try:
        # Path to your ETL script
        script_path = "/content/etl_pipeline.ipynb"
        
        # Execute the ETL script
        result = subprocess.run(["python3", script_path], check=True, capture_output=True, text=True)
        print("✅ ETL pipeline executed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ ETL pipeline execution failed.")
        print("Error:", e.stderr)

if __name__ == "__main__":
    run_etl_pipeline()
