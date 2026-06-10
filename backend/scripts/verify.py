import os
import sys

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

sample = db.query(Email).first()

if sample:

    print("\nSample Email")

    print(
        "Message ID:",
        sample.message_id
    )

    print(
        "Sender:",
        sample.sender
    )

    print(
        "Subject:",
        sample.subject
    )

db.close()