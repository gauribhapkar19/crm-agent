import json
from datetime import datetime, UTC
import sys
import os

# Add backend folder to path
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from databases.db import SessionLocal
from databases.models import Contact

# Create DB session
db = SessionLocal()

# Load JSON file
json_path = os.path.join(
    os.path.dirname(__file__),
    "../../data/email-data-advanced.json"
)

with open(json_path, "r") as f:
    emails = json.load(f)

print(f"Loaded {len(emails)} emails")

# ----------------------------
# Extract unique senders
# ----------------------------

unique_senders = set()

for email in emails:

    sender = email["sender"]

    unique_senders.add(sender)

print(
    f"Found {len(unique_senders)} unique senders"
)

# ----------------------------
# Insert Contacts
# ----------------------------

inserted = 0

for sender in unique_senders:

    existing = db.query(Contact).filter(
        Contact.email == sender
    ).first()

    if existing:
        continue

    domain = sender.split("@")[1]

    company = domain.split(".")[0]

    contact = Contact(
        email=sender,
        company=company,
        status="Active",
        created_at=datetime.now(UTC)
    )

    db.add(contact)

    inserted += 1

db.commit()

print(
    f"Inserted {inserted} contacts"
)

db.close()