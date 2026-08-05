import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey, Boolean, Float, Integer, JSON
)
from sqlalchemy.orm import relationship
from vorik_db.connection import Base

def generate_uuid():
    return str(uuid.uuid4())

class UserDB(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="member")
    preferred_language = Column(String, default="english")
    organisation_id = Column(String, ForeignKey("organisations.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organisation = relationship("OrganisationDB", back_populates="members")
    conversations = relationship("ConversationDB", back_populates="user")

class OrganisationDB(Base):
    __tablename__ = "organisations"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("UserDB", back_populates="organisation")
    workspaces = relationship("WorkspaceDB", back_populates="organisation")

class WorkspaceDB(Base):
    __tablename__ = "workspaces"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    organisation_id = Column(String, ForeignKey("organisations.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    organisation = relationship("OrganisationDB", back_populates="workspaces")

class ConversationDB(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, default="New Conversation")
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    organisation_id = Column(String, nullable=True)
    workspace_id = Column(String, nullable=True)
    pinned = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserDB", back_populates="conversations")
    messages = relationship("MessageDB", back_populates="conversation", cascade="all, delete-orphan")

class MessageDB(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)  # user, assistant, system, tool
    content = Column(Text, nullable=False)
    language = Column(String, nullable=True)
    script = Column(String, nullable=True)
    citations = Column(JSON, default=list)
    model_used = Column(String, nullable=True)
    token_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("ConversationDB", back_populates="messages")

class DocumentDB(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    organisation_id = Column(String, nullable=False)
    workspace_id = Column(String, nullable=False)
    chunk_count = Column(Integer, default=0)
    uploaded_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class CharacterProfileDB(Base):
    __tablename__ = "characters"

    id = Column(String, primary_key=True, default=generate_uuid)
    character_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    age_range = Column(String, nullable=False)
    skin_tone = Column(String, nullable=False)
    face_description = Column(Text, nullable=False)
    hair = Column(String, nullable=False)
    wardrobe = Column(String, nullable=False)
    voice_language = Column(String, nullable=False)
    accent = Column(String, nullable=False)
    personality = Column(Text, nullable=False)
    consent_status = Column(String, default="synthetic")
    organisation_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class MediaJobDB(Base):
    __tablename__ = "media_jobs"

    id = Column(String, primary_key=True, default=generate_uuid)
    job_type = Column(String, nullable=False)  # image, video
    prompt = Column(Text, nullable=False)
    status = Column(String, default="queued")  # queued, processing, completed, failed
    progress = Column(Float, default=0.0)
    output_urls = Column(JSON, default=list)
    error_message = Column(Text, nullable=True)
    user_id = Column(String, nullable=False)
    organisation_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatasetRecordDB(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, default=generate_uuid)
    dataset_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    version = Column(String, default="1.0.0")
    language = Column(String, nullable=False)
    script = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    license_name = Column(String, nullable=False)
    commercial_use_approved = Column(Boolean, default=False)
    pii_scan_status = Column(String, default="passed")
    copyright_review_status = Column(String, default="approved")
    approved_for_training = Column(Boolean, default=False)
    row_count = Column(Integer, default=0)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TrainingJobDB(Base):
    __tablename__ = "training_jobs"

    id = Column(String, primary_key=True, default=generate_uuid)
    job_name = Column(String, nullable=False)
    training_type = Column(String, nullable=False)  # sft, lora, qlora
    base_model = Column(String, nullable=False)
    dataset_id = Column(String, nullable=False)
    status = Column(String, default="queued")  # queued, training, completed, failed
    epochs = Column(Integer, default=3)
    loss_history = Column(JSON, default=list)
    adapter_output_path = Column(String, nullable=True)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ModelRecordDB(Base):
    __tablename__ = "models"

    id = Column(String, primary_key=True, default=generate_uuid)
    model_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    base_model = Column(String, nullable=False)
    version = Column(String, default="1.0.0")
    status = Column(String, default="draft")  # draft, training, staging, canary, production
    deployment_stage = Column(String, default="staging")
    supported_languages = Column(JSON, default=list)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
