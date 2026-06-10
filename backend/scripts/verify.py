import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from databases.db import SessionLocal
from databases.models import (
    Contact,
    Thread,
    Email
)

db = SessionLocal()

print("=" * 40)

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

print("=" * 40)