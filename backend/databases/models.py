from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from db import Base


class Contact(Base):

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True, nullable=False)

    name = Column(String)

    company = Column(String)

    status = Column(String, default="Active")

    created_at = Column(DateTime)

    last_contact_at = Column(DateTime)


class Thread(Base):

    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)

    thread_id = Column(String, unique=True)

    subject = Column(Text)

    sender_email = Column(String)

    first_seen_at = Column(DateTime)

    last_updated_at = Column(DateTime)

    status = Column(String, default="Open")


class Email(Base):

    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)

    message_id = Column(String, unique=True)

    thread_fk = Column(
        Integer,
        ForeignKey("threads.id")
    )

    sender = Column(String)

    subject = Column(Text)

    body = Column(Text)

    timestamp = Column(DateTime)

    status = Column(
        String,
        default="Received"
    )