import json
import os

DB_FILE = "db.json"

def load_db():
    # Load existing DB or start empty
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    else:
        return {}
    
def upload(id, context):
    db = load_db()

    db[id] = context

    # Save back
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def fetch(id):
    db = load_db()

    return db[id]