#!/usr/bin/env python3
"""
calls_data_ingest.py

Generates and inserts mock call-log records into a MongoDB collection.

Fields per document:
 - call_id       : UUID4
 - caller        : fake phone number
 - callee        : fake phone number
 - call_type     : "incoming", "outgoing", or "missed"
 - status        : "completed", "failed", or "no-answer"
 - start_time    : datetime of call start (within last 30 days)
 - end_time      : datetime of call end (start_time + duration)
 - duration_sec  : integer seconds (0 for missed/failed)
 - cost_usd      : float cost (e.g. $0.01/sec for completed calls)
"""

import os
import uuid
import random
from datetime import datetime, timedelta

from pymongo import MongoClient
from faker import Faker

fake = Faker()

def make_call_record():
    # Random start in the past 30 days
    start = datetime.utcnow() - timedelta(days=random.uniform(0, 30),
                                          hours=random.uniform(0, 24),
                                          minutes=random.uniform(0, 60),
                                          seconds=random.uniform(0, 60))
    # Determine call outcome
    call_type = random.choice(["incoming", "outgoing", "missed"])
    status = random.choices(
        ["completed", "failed", "no-answer"],
        weights=[0.7, 0.1, 0.2],
        k=1
    )[0]

    # Duration only if completed
    if status == "completed":
        # between 30 seconds and 2 hours
        duration = random.randint(30, 2 * 3600)
        cost = round(duration * 0.01, 2)  # $0.01 per second
        end = start + timedelta(seconds=duration)
    else:
        duration = 0
        cost = 0.0
        end = start

    return {
        "call_id": str(uuid.uuid4()),
        "caller": fake.phone_number(),
        "callee": fake.phone_number(),
        "call_type": call_type,
        "status": status,
        "start_time": start,
        "end_time": end,
        "duration_sec": duration,
        "cost_usd": cost,
    }

def main():
    # Config via environment or defaults
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    NUM_CALLS = int(os.getenv("NUM_CALLS", 1000))

    client = MongoClient(MONGO_URI)
    db = client["my_app"]
    coll = db["calls"]

    # Generate and insert
    docs = [make_call_record() for _ in range(NUM_CALLS)]
    result = coll.insert_many(docs)
    print(f"Inserted {len(result.inserted_ids)} call records into '{coll.full_name}'")

    client.close()

if __name__ == "__main__":
    main()
