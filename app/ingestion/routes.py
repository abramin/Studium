"""Routes for managing user sources."""

import os
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user_id
from app.config import settings
from app.database import get_db
from app.ingestion.models import Source
from app.ingestion.schemas import SourceResponse

router = APIRouter(prefix="/v1/sources", tags=["sources"])


async def _persist_upload_file(upload: UploadFile, destination_dir: str) -> tuple[str, int]:
    """Save the uploaded file to disk and return its path and size."""

    os.makedirs(destination_dir, exist_ok=True)
    file_extension = Path(upload.filename or "").suffix
    unique_name = f"{uuid.uuid4()}{file_extension}"
    target_path = Path(destination_dir) / unique_name

    file_bytes = await upload.read()
    target_path.write_bytes(file_bytes)

    return str(target_path), len(file_bytes)


@router.get("", response_model=List[SourceResponse])
async def list_sources(db: AsyncSession = Depends(get_db)) -> List[SourceResponse]:
    """List all sources for the current user."""

    current_user_id = get_current_user_id()
    result = await db.execute(
        select(Source)
        .where(Source.owner_user_id == current_user_id)
        .order_by(Source.created_at.desc())
    )
    sources = result.scalars().all()
    return [SourceResponse.model_validate(source) for source in sources]


@router.get("/{source_id}", response_model=SourceResponse)
async def get_source_detail(
    source_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> SourceResponse:
    """Fetch a single source by ID."""

    source = await db.get(Source, source_id)
    if source is None or source.owner_user_id != get_current_user_id():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")

    return SourceResponse.model_validate(source)


@router.post("", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
async def create_source(
    title: str = Form(...),
    description: str | None = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> SourceResponse:
    """Upload a PDF and create a source record."""

    if file.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF uploads are supported at this time.",
        )

    file_path, file_size = await _persist_upload_file(file, settings.UPLOAD_DIR)

    source = Source(
        title=title,
        description=description,
        original_file_name=file.filename or "uploaded.pdf",
        content_type=file.content_type or "application/pdf",
        file_path=file_path,
        file_size=file_size,
        owner_user_id=get_current_user_id(),
    )

    db.add(source)
    await db.flush()

    return SourceResponse.model_validate(source)
