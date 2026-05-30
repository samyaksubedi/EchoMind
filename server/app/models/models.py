# app/models/models.py

from datetime import datetime, timezone
from uuid import uuid4
import enum

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Enum,
    Text,
    JSON,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.databases.postgres_db import Base


# ───────────────────────────────────────────
# Utilities
# ───────────────────────────────────────────


def generate_uuid():
    return uuid4()


def utc_now():
    return datetime.now(timezone.utc)


# ───────────────────────────────────────────
# Enums
# ───────────────────────────────────────────


class SourceType(enum.Enum):
    youtube = "youtube"
    video = "video"
    audio = "audio"
    pdf = "pdf"


class ConversationStatus(enum.Enum):
    uploading = "uploading"
    processing = "processing"
    ready = "ready"
    failed = "failed"


class MessageRole(enum.Enum):
    user = "user"
    assistant = "assistant"


# ───────────────────────────────────────────
# User
# ───────────────────────────────────────────


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)

    name = Column(String, nullable=False)

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(String, nullable=False)

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # email verification

    email_verification_token = Column(String, nullable=True)

    email_verification_token_expires = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # password reset

    reset_password_token = Column(String, nullable=True)

    reset_password_token_expires = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    # relationships

    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    sessions = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# ───────────────────────────────────────────
# Conversation
# ───────────────────────────────────────────


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)

    title = Column(String, nullable=False)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    # source info

    source_link = Column(String, nullable=True)

    source_type = Column(
        Enum(SourceType),
        nullable=False,
    )

    status = Column(
        Enum(ConversationStatus),
        default=ConversationStatus.uploading,
        nullable=False,
    )

    # temp paths

    temp_source_path = Column(String, nullable=True)

    temp_audio_path = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    # relationships

    user = relationship(
        "User",
        back_populates="conversations",
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )


# ───────────────────────────────────────────
# Message
# ───────────────────────────────────────────


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)

    conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id"),
        nullable=False,
    )

    role = Column(
        Enum(MessageRole),
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    # null for user messages
    # {startTime, endTime}
    # {pageNumber}

    source_reference = Column(
        JSON,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    # relationships

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )


# ───────────────────────────────────────────
# UserSession
# ───────────────────────────────────────────


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    refresh_token = Column(
        String,
        nullable=False,
    )

    device_info = Column(
        String,
        nullable=True,
    )

    ip_address = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    last_used_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    # relationships

    user = relationship(
        "User",
        back_populates="sessions",
    )
