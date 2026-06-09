# create_tables.py

from db import Base, engine
from models import *

Base.metadata.create_all(bind=engine)

print("Database Created")