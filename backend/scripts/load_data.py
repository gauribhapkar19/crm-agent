import json
import os
import sys

from datetime import datetime, UTC

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
from databases.models import Thread
from databases.models import Email

db = SessionLocal()

# ==========================================
# LOAD JSON
# ==========================================

json_path = os.path.join(
    os.path.dirname(__file__),
    "../../data/email-data-advanced.json"
)

with open(json_path, "r") as f:
    emails = json.load(f)

print(f"\nLoaded {len(emails)} emails")

# ==========================================
# GENERATE CONTACTS
# ==========================================

unique_senders = set()

for email in emails:
    unique_senders.add(email["sender"])

print(
    f"Found {len(unique_senders)} unique senders"
)

contact_inserted = 0

for sender in unique_senders:

    existing = db.query(Contact).filter(
        Contact.email == sender
    ).first()

    if existing:
        continue

    company = sender.split("@")[1].split(".")[0]

    contact = Contact(
        email=sender,
        company=company,
        status="Active",
        created_at=datetime.now(UTC)
    )

    db.add(contact)

    contact_inserted += 1

db.commit()

print(
    f"Inserted {contact_inserted} contacts"
)

# ==========================================
# GENERATE THREADS
# ==========================================

unique_threads = {}

for email in emails:

    thread_id = email["thread_id"]

    if thread_id not in unique_threads:
        unique_threads[thread_id] = email

thread_inserted = 0

for thread_id, email_data in unique_threads.items():

    existing = db.query(Thread).filter(
        Thread.thread_id == thread_id
    ).first()

    if existing:
        continue

    thread = Thread(
        thread_id=thread_id,
        subject=email_data["subject"],
        sender_email=email_data["sender"],
        first_seen_at=datetime.now(UTC),
        last_updated_at=datetime.now(UTC),
        status="Open"
    )

    db.add(thread)

    thread_inserted += 1

db.commit()

print(
    f"Inserted {thread_inserted} threads"
)

# ==========================================
# INSERT EMAILS
# ==========================================

email_inserted = 0

for email_data in emails:

    existing = db.query(Email).filter(
        Email.message_id ==
        email_data["message_id"]
    ).first()

    if existing:
        continue

    thread = db.query(Thread).filter(
        Thread.thread_id ==
        email_data["thread_id"]
    ).first()

    email = Email(
        message_id=email_data["message_id"],
        sender=email_data["sender"],
        subject=email_data["subject"],
        body=email_data["body"],
        timestamp=datetime.fromisoformat(
            email_data["timestamp"]
            .replace("Z", "+00:00")
        ),
        thread_fk=thread.id,
        status="Received"
    )

    db.add(email)

    email_inserted += 1

db.commit()

print(
    f"Inserted {email_inserted} emails"
)

# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n" + "=" * 50)

print(
    "Contacts:",
    db.query(Contact).count()
)

print(
    "Threads:",
    db.query(Thread).count()
)

print(
    "Emails:",
    db.query(Email).count()
)

print("=" * 50)

db.close()