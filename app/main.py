"""
Studium - A strict-evidence learning companion.

Main application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.ingestion.routes import router as sources_router

app = FastAPI(
    title="Studium API",
    description="A strict-evidence learning companion that turns your sources into a mastery-driven study loop",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sources_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Studium API",
        "version": "0.1.0",
        "status": "ready",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "studium-api",
    }


# Future module routers will be included here:
# from app.ingestion.routes import router as ingestion_router
# from app.retrieval.routes import router as retrieval_router
# from app.tutor.routes import router as tutor_router
# from app.quiz.routes import router as quiz_router
# from app.mastery.routes import router as mastery_router
#
# app.include_router(ingestion_router, prefix="/api/v1/ingestion", tags=["ingestion"])
# app.include_router(retrieval_router, prefix="/api/v1/retrieval", tags=["retrieval"])
# app.include_router(tutor_router, prefix="/api/v1/tutor", tags=["tutor"])
# app.include_router(quiz_router, prefix="/api/v1/quiz", tags=["quiz"])
# app.include_router(mastery_router, prefix="/api/v1/mastery", tags=["mastery"])
