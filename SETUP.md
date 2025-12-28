# Studium - Getting Started

## Quick Start with Docker

The easiest way to get started is using Docker Compose, which sets up the entire stack.

### Prerequisites

- Docker and Docker Compose installed
- (Optional) OpenAI API key for AI features

### Setup Steps

1. **Clone the repository** (if not already done)
   ```bash
   git clone https://github.com/abramin/Studium.git
   cd Studium
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Add your OpenAI API key** (optional for initial testing)
   
   Edit `.env` and set:
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```

4. **Start the stack**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - **API** on http://localhost:8000
   - **PostgreSQL** with pgvector on port 5432
   - **Redis** on port 6379
   - **MinIO** (S3-compatible storage) on http://localhost:9000
   - **MinIO Console** on http://localhost:9001
   - **Celery Worker** for background tasks
   - **Flower** (Celery monitoring) on http://localhost:5555

5. **Verify the setup**
   ```bash
   curl http://localhost:8000/health
   ```

   You should see:
   ```json
   {"status":"healthy","service":"studium-api"}
   ```

6. **View logs**
   ```bash
   docker-compose logs -f api
   ```

7. **Stop the stack**
   ```bash
   docker-compose down
   ```

   To also remove volumes:
   ```bash
   docker-compose down -v
   ```

## Development Setup (without Docker)

If you prefer to run without Docker:

### Prerequisites

- Python 3.12+
- PostgreSQL 17 with pgvector extension
- Redis

### Setup Steps

1. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your local database credentials
   ```

4. **Run the API**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Run Celery worker** (in a separate terminal)
   ```bash
   celery -A app.celery_worker.celery_app worker --loglevel=info
   ```

## Testing

Run tests with pytest:

```bash
# Install dev dependencies if not already installed
pip install -r requirements.txt

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing
```

## Code Quality

### Formatting with Black

```bash
black app tests
```

### Linting with Ruff

```bash
ruff check app tests
```

### Type Checking with MyPy

```bash
mypy app
```

## API Documentation

Once the API is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Stack Overview

| Service | Purpose | Port | Access |
|---------|---------|------|--------|
| FastAPI | Backend API | 8000 | http://localhost:8000 |
| PostgreSQL | Database with pgvector | 5432 | localhost:5432 |
| Redis | Cache & Message Broker | 6379 | localhost:6379 |
| MinIO | S3-compatible storage | 9000 | http://localhost:9000 |
| MinIO Console | Storage admin UI | 9001 | http://localhost:9001 |
| Flower | Celery task monitor | 5555 | http://localhost:5555 |

### Default Credentials

**PostgreSQL:**
- User: `studium`
- Password: `studium_dev_password`
- Database: `studium`

**MinIO:**
- Access Key: `minioadmin`
- Secret Key: `minioadmin`
- Bucket: `studium-sources`

**Note:** These are development credentials. Change them for production use.

## Project Structure

```
Studium/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup
│   ├── celery_worker.py     # Celery configuration
│   ├── ingestion/           # Source ingestion module
│   ├── retrieval/           # Search and retrieval module
│   ├── tutor/               # Tutoring mode module
│   ├── quiz/                # Quiz generation module
│   ├── mastery/             # Mastery tracking module
│   └── eval/                # Evaluation module
├── tests/
│   └── test_api.py          # API tests
├── docs/
│   └── prd.md               # Product requirements
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Stack orchestration
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project metadata & tools config
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Next Steps

This is the initial bootstrap. The modules (`ingestion`, `retrieval`, `tutor`, `quiz`, `mastery`, `eval`) are placeholder directories. Functionality will be implemented in future phases according to `docs/prd.md`.

For feature development, see the MVP scope in `docs/prd.md`.
