import uuid

from sqlalchemy import Column, String, Boolean, Text 
from sqlalchemy.dialects.postgresql import UUID
from app.database.database import Base 

class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4 
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    completed = Column(
        Boolean,
        default=False,
        nullable=False
    )

