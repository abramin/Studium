# Studium

A learning companion that helps you **actually remember** what you study.

Bring your own materials (PDFs, links, notes) and study in focused sessions with:
- **strict citations by default**
- **adaptive quizzes**
- **mastery tracking**
- **30-minute sessions** that pick what matters most next

---

## What Studium does

### 1) Turns your materials into a tutor
Add sources:
- PDFs (textbooks, papers, slide decks)
- web pages (articles, docs, research posts)
- notes (paste text, markdown)

Ask questions, get explanations, and always see where the answer came from.

### 2) Keeps you honest with strict evidence
Studium is **strict-evidence by default**:
- factual claims are backed by citations from your sources
- you get short snippets so you can verify quickly
- if your sources do not cover something, it says so

Optional: allow **Uncited general knowledge** (clearly labeled), or disable it entirely.

### 3) Builds mastery over time
Instead of “chat history”, you get progress:
- concepts and prerequisites
- mastery score per concept
- what you keep missing
- what you’re likely to forget next
- a clear “what to study next” recommendation

### 4) Runs a 30-minute study session for you
Default session structure:
- **5 min** recap (due reviews + last misses)
- **15 min** learn/strengthen (Socratic-first)
- **10 min** quiz (graded, updates mastery + schedule)

---

## Who it’s for
- self-directed learners who want **retention**, not just explanations
- students studying from mixed materials
- professionals learning new domains from docs and papers
- anyone who wants “show me the source” as the default

---

## Example use cases
- “Teach me this chapter, then quiz me until I can explain it cleanly.”
- “Summarize the key claims and link each one to the exact source.”
- “I have 30 minutes. What should I review right now?”
- “Diagnose why I keep confusing concept A and B, using my materials.”

---

## Product principles

### Mastery over messages
Progress is the product: what you know, what you don’t, and what to do next.

### Evidence over vibes
If it can’t retrieve support from your sources, it should not pretend.

### Practice beats rereading
Quizzes and recall drive learning more than passive review.

---

## Status
**Project bootstrapped!** The development environment is set up with Docker and basic FastAPI structure.

Planned milestones:
- **Phase 1:** source ingestion, strict-cited tutoring, basic quizzes, spaced repetition
- **Phase 2:** concept graph, adaptive sessions, mastery dashboard, evaluation harness
- **Phase 3:** richer quiz types, misconception detection, improved retrieval/reranking

### Getting Started

See [SETUP.md](SETUP.md) for detailed setup instructions.

**Quick start:**
```bash
# Validate the setup
python validate.py

# Start with Docker
docker compose up -d

# Pull Ollama models
docker exec -it studium-ollama ollama pull llama3.2
docker exec -it studium-ollama ollama pull nomic-embed-text

# Visit the API
open http://localhost:8000/docs
```

**Tech Stack:**
- Python 3.12+ with FastAPI
- PostgreSQL 17 with pgvector
- Redis 7
- Ollama (local LLM & embeddings)
- Local filesystem storage
- Celery for background jobs

---

## Privacy (intent)
Your sources are your data.
The goal is strong isolation and a clear “delete my data” path from day one.

---

## Name
**Studium**: a medieval workshop for reading, copying, and study.
This app is the same idea, but interactive and mastery-driven.

---

## Feedback
If you try it, the most useful feedback is:
- what you studied (type of material)
- where citations felt missing or wrong
- whether the session structure works for you
- what “mastery” means in your context (exam, job skills, long-term retention)

License: TBD
