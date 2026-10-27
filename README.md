# Rural FMCG Insights — Shelf-Signal

## Problem Understanding

FMCG companies publish annual reports containing information about rural demand, pricing strategies, product launches, distribution, and market growth. These reports can be hundreds of pages long, making it difficult for sales officers to find relevant information quickly, especially on budget smartphones with slow internet connections.

Sales officers at FMCG distributors need quick, reliable information from company reports to understand market strategies and make better rural stock-planning decisions.

## Proposed Solution

Shelf-Signal is a mobile-friendly assistant designed to answer questions about FMCG company reports.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from annual reports and provide concise answers with company, report, and page references.

The goal is to reduce the time and data required to find useful business insights.

## Report Coverage

The project covers six FMCG companies:

- Hindustan Unilever Limited (HUL)
- ITC Limited
- Nestlé India
- Dabur India
- Marico
- Britannia Industries

**Initial dataset:** Six annual reports covering one reporting year per company.

**Current dataset status:**
- 6 PDF reports collected and validated
- 2,053 total PDF pages
- 2,049 pages with extractable text
- PDF text extraction implemented using PyMuPDF
- Extracted page-level records include company name, report year, source filename, page number, and text

**Future target:** Expand coverage to at least 18 annual reports across three years, targeting 6,000+ pages and relevant BRSR documents.

## Key Focus Areas

- Rural market demand and growth
- Pricing changes and product affordability
- New product launches and smaller pack sizes
- Distribution expansion and rural market reach
- Comparison of company strategies across reporting years

## Tech Stack

- **Programming Language:** Python
- **PDF Processing:** PyMuPDF
- **Text Embeddings:** Sentence Transformers
- **Vector Search:** FAISS
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Database:** SQLite
- **AI/LLM:** Retrieval-Augmented Generation (RAG)

## Current Development Status

- [✓]Collect annual reports from six FMCG companies
- [✓]Validate PDF page counts and text extraction
- [✓]Extract page-level text with source metadata
- [ ] Implement text chunking and embeddings
- [ ] Build FAISS-based semantic retrieval
- [ ] Implement LLM-powered question answering
- [ ] Add streaming, retries, timeouts, and fallback handling
- [ ] Implement cost tracking and usage endpoints
- [ ] Configure Docker Compose with PostgreSQL/pgvector
- [ ] Complete CI and deployment

## Expected Outcome

A lightweight, mobile-friendly assistant that turns lengthy corporate reports into concise, source-backed answers. The project aims to help FMCG sales officers understand rural market trends and make better-informed stock-planning decisions.