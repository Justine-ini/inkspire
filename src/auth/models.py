from sqlalchemy.dialects.mysql import TIMESTAMP  # Import MySQL-specific TIMESTAMP
from sqlmodel import SQLModel, Field,  Column
from datetime import datetime
from sqlalchemy import String
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            String(36, collation="utf8_bin"),  # Collation defined in String type
            primary_key=True,
            default=uuid.uuid4,
            nullable=False,
        )
    )
    uid: uuid.UUID
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP, default=datetime.now)
    )


    def __repr__(self):
        return f"<User {self.username}>"