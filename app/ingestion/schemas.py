"""Pydantic schemas for source ingestion."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SourceBase(BaseModel):
    title: str
    description: Optional[str] = None


class SourceCreate(SourceBase):
    pass


class SourceResponse(SourceBase):
    id: UUID
    owner_user_id: Optional[str] = Field(default=None)
    original_file_name: str
    content_type: str
    file_size: int
    file_path: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }
