#!/usr/bin/env python3
"""
export_calls_csv.py

Connects to MongoDB, reads the 'calls' collection, and writes it to a CSV file.

Usage:
  python export_calls_csv.py

Configurable via environment variables:
  MONGO_URI        MongoDB connection string (default: mongodb://localhost:27017)
  DB_NAME          Database name (default: my_app)
  COLLECTION_NAME  Collection name (default: calls)
  OUTPUT_FILE      CSV file to write (default: calls.csv)
"""

import os
import pandas as pd
from pymongo import MongoClient

def main():
    # Load configuration
    MONGO_URI       = os.getenv("MONGO_URI",       "mongodb://localhost:27017")
    DB_NAME         = os.getenv("DB_NAME",         "my_app")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "calls")
    OUTPUT_FILE     = os.getenv("OUTPUT_FILE",     "calls.csv")

    # Connect
    client = MongoClient(MONGO_URI)
    db     = client[DB_NAME]
    coll   = db[COLLECTION_NAME]

    # Fetch all documents
    docs = list(coll.find())
    if not docs:
        print(f"No documents found in `{DB_NAME}.{COLLECTION_NAME}`")
        return

    # Convert to DataFrame
    df = pd.DataFrame(docs)

    # Convert ObjectId and datetimes to strings for CSV
    if '_id' in df.columns:
        df['_id'] = df['_id'].astype(str)
    for dtcol in ('start_time', 'end_time'):
        if dtcol in df.columns:
            df[dtcol] = pd.to_datetime(df[dtcol]).dt.strftime("%Y-%m-%d %H:%M:%S")

    # Write CSV
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Exported {len(df)} records to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
