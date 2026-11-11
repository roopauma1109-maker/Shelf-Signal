# Rural FMCG Insights — ShelfSignal

## Problem Understanding

FMCG companies publish annual reports containing valuable information about rural demand, pricing strategies, product launches, distribution networks, and market growth.

These reports often contain hundreds of pages, making it difficult for sales officers to quickly identify relevant business insights. This becomes especially challenging when they use budget smartphones and have limited internet connectivity.

Sales officers at FMCG distributors need quick and reliable access to company information to understand market strategies and make better-informed rural stock-planning decisions.

## Proposed Solution

**ShelfSignal** is a mobile-friendly, low-bandwidth FMCG annual report research assistant.

It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from company annual reports and generate concise answers with company names, report references, and page numbers.

The system combines semantic and keyword-based retrieval to improve the relevance of retrieved information.

The primary goal is to reduce the time and data required to find useful business insights from lengthy corporate reports.

## Report Coverage

The project currently covers six FMCG companies:

- Hindustan Unilever Limited (HUL)
- ITC Limited
- Nestlé India
- Dabur India
- Marico
- Britannia Industries

**Initial dataset:**
- Six annual reports covering one reporting year per company
- 2,053 total PDF pages
- 2,049 pages with extractable text

**Future target:**

Expand coverage to at least 18 annual reports across three reporting years, targeting 6,000+ pages and relevant Business Responsibility and Sustainability Reports (BRSR).

## Dataset Processing

- PDF text extraction using PyMuPDF
- Page-level text extraction with source metadata
- Company name, report year, source filename, page number, and extracted text retained
- Paragraph-first and sentence-aware text chunking
- 6,277 text chunks generated
- Sentence Transformer embeddings using `all-MiniLM-L6-v2` (384 dimensions)

## Key Focus Areas

- Rural market demand and growth
- Pricing changes and product affordability
- New product launches and smaller pack sizes
- Distribution expansion and rural market reach
- Comparison of company strategies across reporting years

## Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| PDF Processing | PyMuPDF |
| Text Embeddings | Sentence Transformers |
| Semantic Search | FAISS |
| Keyword Search | BM25 |
| Retrieval Ranking | Reciprocal Rank Fusion (RRF) |
| Backend | FastAPI |
| LLM Integration | Google Gemini |
| RAG Architecture | Retrieval-Augmented Generation |
| Containerization | Docker and Docker Compose |
| Database Infrastructure | PostgreSQL with pgvector |

**Note:** Current vector retrieval uses FAISS. PostgreSQL/pgvector is configured in Docker Compose, but pgvector-based vector storage and retrieval integration is still pending.

## Current Development Status

### Completed

- [x] Collect annual reports from six FMCG companies
- [x] Validate PDF page counts and text extraction
- [x] Extract page-level text with source metadata
- [x] Implement paragraph-first, sentence-aware text chunking
- [x] Generate embeddings using Sentence Transformers
- [x] Build FAISS-based semantic retrieval
- [x] Implement BM25 keyword retrieval
- [x] Combine semantic and keyword results using Reciprocal Rank Fusion (RRF)
- [x] Implement LLM-powered question answering using Google Gemini
- [x] Return structured answers with company, report, and page citations
- [x] Implement streaming, timeouts, retries, and fallback model handling
- [x] Implement cost tracking and the `/usage` endpoint
- [x] Configure Docker Compose with FastAPI and PostgreSQL/pgvector
- [x] Add automated tests, code formatting, and pre-commit checks
- [x] Configure CI workflow

### In Progress / Pending

- [ ] Complete pgvector-based vector storage and retrieval integration
- [ ] Verify parser heading preservation
- [ ] Implement and validate the `/ask` endpoint if required
- [ ] Create `docs/EVAL_v0.md` and evaluate the system using 10 real questions
- [ ] Complete deployment verification and update the live demo documentation

## Expected Outcome

A lightweight, mobile-friendly assistant that transforms lengthy FMCG annual reports into concise, source-backed business insights.

ShelfSignal aims to help rural FMCG sales officers quickly understand market trends, product affordability, pricing strategies, and distribution expansion so they can make better-informed stock-planning decisions, even with limited internet connectivity.
