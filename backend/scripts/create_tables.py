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

from databases.db import Base, engine
from databases.models import *

Base.metadata.create_all(bind=engine)

print("Database Created Successfully")