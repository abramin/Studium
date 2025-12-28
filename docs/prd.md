# PRD: Studium (AI Learning Companion)

A strict-evidence learning companion that turns your sources into a mastery-driven study loop.

Studium ingests PDFs, web pages, and notes, then helps you **learn, practice, and retain** with:
- source-grounded tutoring (citations by default)
- adaptive quizzes
- concept mastery tracking
- scheduled 30-minute study sessions

> North star: better retention over weeks, not prettier chat over minutes.

This PRD updates the earlier repo draft :contentReference[oaicite:0]{index=0} with **SPA + OIDC auth from day one**, and **local storage first** (S3 later).

---

## 1) Goals
- Help users **retain** knowledge over weeks through recall, quizzes, and spaced repetition.
- Default to **strict evidence**: answers cite user-provided sources with snippets.
- Track **mastery/progress** per concept and recommend the next best study action.
- Be deployable as a real product: **auth, API boundaries, data isolation**.

## 2) Non-goals
- Not a general chatbot replacement.
- Not a full LMS (classes, grading workflows).
- Not “answer anything” without sources. When coverage is missing, say so.

---

## 3) Target users and scenarios
**Users:** self-directed learners (students or professionals) studying from mixed materials.

**Scenarios**
- “Teach me this topic from these PDFs and links. Cite everything.”
- “I have 30 minutes, tell me what to review for the biggest progress.”
- “Quiz me and track what I’m weak at, then schedule review.”

---

## 4) Product principles

## Strict evidence by default
Default behavior is **Strict Evidence ON** and **Uncited General Knowledge OFF**.

- The assistant may only make factual claims that are supported by retrieved source chunks.
- Every supported claim includes citations and short quote snippets.
- If retrieval does not support an answer, the assistant must:
  - state that the sources are insufficient,
  - ask a targeted clarification question or request additional sources,
  - optionally propose what kind of source would resolve the gap.

### Settings
- `allow_uncited_general_knowledge`: default `false`
- If enabled by the user, uncited content must be clearly separated and labeled.

### Acceptance criteria
- No response contains unlabeled content that is not supported by retrieved chunks.
- No citations are fabricated; every citation maps to a stored chunk id.
- When sources lack coverage, the assistant refuses to speculate and instead requests sources/clarification.


### Mastery over messages
Progress is first-class:
- mastery per concept (0–1)
- decay/stability over time
- misconception tags (optional)
- evidence strength per concept

### 30-minute sessions
Default structure:
- **5 min** recap (due reviews + last misses)
- **15 min** learn/strengthen (Socratic-first)
- **10 min** quiz block (graded, updates mastery + schedule)

---

## 5) MVP Scope (Phase 1)
### Collections (general, not OU-specific)
- Create “Collections” (e.g., “Neuroscience”, “Go Concurrency”, “Chapter 3”)
- Add sources to a collection and filter study by collection

### Source ingestion
- PDF upload
- URL add (ingest content)
- Notes (paste/markdown)

### Parse Quality Report per source
- extraction coverage and errors
- detected headings/structure (when possible)
- warnings (garbled text, empty pages, etc.)

### RAG answering with citations + quote snippets
- strict evidence formatting
- clickable citations that open source snippet context

### Tutor modes
- Lesson mode
- Socratic mode

### Quizzes
- Flashcards
- Short answer
- Store attempts

### Basic spaced repetition scheduling
- SM-2 style scheduling baseline
- “Start session” returns due items and weak concepts

---

## 6) Phase 2 (Proposal B core)
- Concept graph + prerequisites
- Mastery model + adaptive session selection
- Study plans + dashboard
- Evaluation harness + CI gates for retrieval/citation quality

---

## 7) Platform decisions (updated)
### Frontend
- **SPA:** Next.js (TypeScript)
- Pages (MVP):
  - `/login` (provider hosted or embedded)
  - `/collections`
  - `/sources` (list + add)
  - `/sources/:id` (preview + parse report)
  - `/chat` (collection-scoped)
  - `/quiz` (generate + take)

### Storage
- **Local storage first** for PDFs (dev speed)
- Clean abstraction so later you can switch to **S3**:
  - future plan: backend issues **pre-signed URLs** or streams uploads
  - keep file metadata stable so storage backend is swappable

---

## 8) Architecture (early sketch)
**Backend:** Python (FastAPI)  
**DB:** Postgres + pgvector  
**Cache:** Redis (optional in Phase 1; useful for sessions/retrieval caching later)  
**Jobs:** Celery (upgrade path: Temporal)  
**Storage:** Local filesystem (Phase 1), S3-compatible later

High-level modules:
- `auth` (JWKS verification, user context)
- `ingestion` (parse → clean → chunk → embed → index)
- `retrieval` (hybrid search + optional rerank)
- `tutor` (modes + strict evidence formatting)
- `quiz` (generate/score/schedule)
- `mastery` (concept + updates)
- `eval` (datasets + CI regression)

---

## 9) Data model (high-level)
All entities include: `id`, `owner_user_id`, `created_at`, `updated_at`

- Collection
- Source (type: pdf|url|note, title, status)
- ParseReport (per source)
- SourceChunk (text, embedding, source_location)
- Conversation + Message (collection-scoped)
- Quiz (generated set) + QuizItem
- QuizAttempt
- ReviewScheduleItem
- Concept + ConceptEvidence (Phase 2)
- MasteryState (Phase 2)

---

## 10) RAG behavior (strict evidence)
Pipeline:
1. retrieve chunks (vector + keyword)
2. dedupe/diversify
3. generate answer with citations
4. post-check: cited sentences must map to chunk ids

If retrieval confidence is low:
- explicitly say “insufficient source coverage”
- suggest which source to add or ask a clarifying question

---

## 11) Evaluation (Phase 2 requirement, but seed early)
- Start collecting “golden questions” per collection
- Metrics:
  - citation precision (do citations support the sentence?)
  - unsupported claim rate
  - retrieval recall on golden set
- CI gate later: fail on regressions

---

## 12) Security and privacy (MVP baseline)
- OIDC auth required for all endpoints (except health/login bootstrap)
- DB scoping by `owner_user_id` at query level (and ideally constraints)
- “Delete my data” endpoint removes:
  - sources + files
  - chunks/embeddings
  - conversations
  - quiz attempts/schedules

---

## 13) Build plan as vertical slices (SPA + API)
Each slice is a clickable demo.

1. **Source Library**: auth + upload/list/get sources (local storage)
2. **Parse + Preview**: background parse + source detail preview + parse report
3. **Ask with Citations**: chunk/embed + chat + clickable citations/snippets
4. **Tutor Modes**: lesson vs socratic toggle
5. **Quiz Generator**: flashcards + short answer + stored attempts
6. **Spaced Repetition Queue**: due items + “start 30-min session”
7. **Collections**: group sources and scope chat/quiz by collection
8. **URL + Notes ingestion**: full ingestion parity across source types

---

## 14) Requirements (dev)
- Python 3.14+
- Postgres (with pgvector)
- Node 18+ (Next.js)
- Optional: Redis (if enabling background queue/caching early)

---
