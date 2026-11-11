# ShelfSignal – Progress Tracker

## Week 1 (tag week-1 by Fri 23 Oct)

- [x] Repo created from the Examate template and registered on the form
- [x] README top section filled from my project card
- [x] `/health` runs locally
- [x] `docs/QUESTIONS.md`: 10 real questions
- [x] 50+ pages collected, DATASET.md filled, sample in data/sample/
- [x] Tag week-1 pushed

## Week 2 (tag week-2 by Fri 30 Oct)

- [x] POST `/chat` calls an LLM and returns structured JSON
- [x] Streaming, timeouts, retry and a fallback model
- [x] Cost log + GET `/usage`
- [x] Docker Compose (API + Postgres/pgvector) runs
- [x] CI green, live link in README
- [x] Tag week-2 pushed

## Week 3 (tag week-3 by Fri 6 Nov)

- [~] Parser preserves page numbers; heading preservation needs verification
- [~] 500+ pages chunked and embedded (6,277 chunks); FAISS storage implemented, pgvector storage pending
- [~] POST `/chat` returns answers with document and page citations; `/ask` endpoint pending
- [ ] `docs/EVAL_v0.md` with 10 questions scored
- [ ] Tag week-3 pushed

## Daily log

| Date | What I did today | Commit |
|---|---|---|
| 4 Nov 2026 | Added pre-commit hooks, formatting and validation; all 10 tests passed
| 11 Nov 2026 | Updated Gemini timeout, retry configuration and output token limit; Ruff passed and all 10 tests passed. Docker rebuild started; verification pending
