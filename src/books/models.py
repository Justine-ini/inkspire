from sqlmodel import SQLModel, Field, Column
from sqlalchemy import UUID, String  # Import UUID from SQLAlchemy
from sqlalchemy.dialects.mysql import TIMESTAMP  # Import MySQL-specific TIMESTAMP
import uuid
from datetime import date, datetime

class Book(SQLModel, table=True):
    __tablename__ = "books"
    
    # Store UUID as CHAR(36) with collation
    uid: uuid.UUID = Field(
        sa_column=Column(
            String(36, collation="utf8_bin"),  # Collation defined in String type
            primary_key=True,
            default=uuid.uuid4,
            nullable=False,
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP, default=datetime.now)
    )

    def __repr__(self):
        return f"<Book {self.title}>"