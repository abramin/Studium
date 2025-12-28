"""
Celery worker configuration.
"""

from celery import Celery

from app.config import settings

celery_app = Celery(
    "studium",
    broker=settings.celery_broker,
    backend=settings.celery_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)

# Auto-discover tasks from installed apps
celery_app.autodiscover_tasks(
    [
        "app.ingestion",
        "app.retrieval",
        "app.quiz",
        "app.mastery",
    ]
)


@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing."""
    print(f"Request: {self.request!r}")
