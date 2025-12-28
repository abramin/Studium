# Studium

A strict-evidence learning companion that turns your sources into a mastery-driven study loop.

Studium ingests PDFs, web pages, and notes, then helps you **learn, practice, and retain** with:
- source-grounded tutoring (citations by default)
- adaptive quizzes
- concept mastery tracking
- scheduled 30-minute study sessions

> North star: better retention over weeks, not prettier chat over minutes.

---

## Why this exists

Most “AI tutors” are good at explaining and bad at ensuring you actually remember anything later.

Studium is built around a tight loop:

1. **Ingest** sources (PDFs, URLs, notes)  
2. **Teach** with strict citations  
3. **Test** recall and transfer  
4. **Track** mastery by concept  
5. **Schedule** the next review session automatically

---

## Key ideas

### Strict evidence by default
- Factual claims should be backed by your sources.
- If retrieval is weak, Studium says so.
- Anything not supported is labeled **Uncited general knowledge** (configurable).

### Mastery, not messages
Studium models learning progress explicitly:
- mastery per concept (0–1)
- decay/stability over time
- misconception tags (optional)
- evidence strength (how well a concept is covered by sources)

### 30-minute sessions
Default session structure:
- **5 min** recap (due reviews + last misses)
- **15 min** learn/strengthen (Socratic-first)
- **10 min** quiz block (graded, updates mastery + schedule)

---

## MVP scope (Phase 1)
- [ ] Course/Week organization (OU-friendly)
- [ ] Source ingestion: PDF + URL + notes
- [ ] Parse Quality Report per source
- [ ] RAG answering with citations + quote snippets
- [ ] Tutor modes: Lesson + Socratic
- [ ] Quizzes: flashcards + short answer
- [ ] Basic spaced repetition scheduling

## Proposal B core (Phase 2)
- [ ] Concept graph + prerequisites
- [ ] Mastery model + adaptive session selection
- [ ] Study plans + dashboard
- [ ] Evaluation harness + CI gates for retrieval/citation quality

---

## Architecture (early sketch)

**Backend:** Python (FastAPI)  
**DB:** Postgres + pgvector  
**Cache:** Redis  
**Jobs:** Celery (upgrade path: Temporal)  
**Storage:** S3-compatible for PDFs

High-level modules:
- `ingestion` (parse → chunk → embed → index)
- `retrieval` (hybrid search + rerank)
- `tutor` (modes + strict evidence formatting)
- `quiz` (generate/score/schedule)
- `mastery` (concept graph + updates)
- `eval` (datasets + metrics + CI regression)

---

## Getting started (placeholder)

### Requirements
- Python 3.14+
- Postgres (with pgvector)
- Redis

### Setup
```bash
# create venv
python -m venv .venv
source .venv/bin/activate

# install deps
pip install -r requirements.txt

# run api
uvicorn app.main:app --reload
