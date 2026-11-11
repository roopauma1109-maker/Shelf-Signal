# ShelfSignal Dataset

## Project Overview

ShelfSignal collects annual reports from six FMCG companies to support research on rural growth, pricing strategies, distribution, and business performance.

The reports are stored as PDF files in the `data/sample/` directory and serve as the source documents for the ShelfSignal RAG pipeline.

## Collected Reports

| S.No. | Company | Report | File Path |
|---:|---|---|---|
| 1 | Hindustan Unilever Limited (HUL) | Annual Report 2025–26 | `data/sample/HUL/HUL-2025-26.pdf` |
| 2 | ITC Limited | Annual Report 2025–26 | `data/sample/ITC/ITC-2025-26.pdf` |
| 3 | Nestlé India | Annual Report 2025–26 | `data/sample/Nestle_India/Nestle-2025-26.pdf` |
| 4 | Dabur India | Annual Report 2025–26 | `data/sample/Dabur/Dabur-2025-26.pdf` |
| 5 | Marico Limited | Annual Report 2025–26 | `data/sample/Marico/Marico-2025-26.pdf` |
| 6 | Britannia Industries | Annual Report 2025–26 | `data/sample/Britannia/Britannia-2025-26.pdf` |

## Dataset Directory Structure

```text
Shelf-Signal/
├── data/
│   └── sample/
│       ├── HUL/
│       │   └── HUL-2025-26.pdf
│       ├── ITC/
│       │   └── ITC-2025-26.pdf
│       ├── Nestle_India/
│       │   └── Nestle-2025-26.pdf
│       ├── Dabur/
│       │   └── Dabur-2025-26.pdf
│       ├── Marico/
│       │   └── Marico-2025-26.pdf
│       └── Britannia/
│           └── Britannia-2025-26.pdf
├── DATASET.md
├── PROGRESS.md
└── README.md
```

## Companies Covered

The dataset covers six FMCG companies:

1. Hindustan Unilever Limited (HUL)
2. ITC Limited
3. Nestlé India
4. Dabur India
5. Marico Limited
6. Britannia Industries

## Dataset Inventory

| Company | Report Year | Total Pages | Pages with Extractable Text |
|---|---|---:|---:|
| Britannia | 2025–26 | 189 | 189 |
| Dabur | 2025–26 | 623 | 622 |
| HUL | 2025–26 | 244 | 244 |
| ITC | 2025–26 | 412 | 411 |
| Marico | 2025–26 | 279 | 279 |
| Nestlé India | 2025–26 | 306 | 304 |
| **Total** | | **2,053** | **2,049** |

## Data Collection Notes

- Annual report PDFs from six FMCG companies are organized by company.
- Each report is stored in its respective company folder under `data/sample/`.
- The reporting year is included in each PDF filename.
- All six PDFs have been checked for page counts and text extraction.
- A total of 2,053 PDF pages were identified.
- Extractable text is available on 2,049 pages.
- Four pages do not contain extractable text.
- PDF extraction is implemented using PyMuPDF.
- Page-level extracted records retain company name, report year, source filename, page number, and text.
- The collected reports are used for researching FMCG rural growth, sales performance, pricing, and distribution strategies.

## Text Processing and Retrieval Status

- [x] PDF text extraction using PyMuPDF
- [x] Page-level metadata preservation
- [x] Paragraph-first and sentence-aware chunking
- [x] 6,277 text chunks generated
- [x] Text embeddings generated using `all-MiniLM-L6-v2` (384 dimensions)
- [x] FAISS semantic index created
- [x] BM25 keyword retrieval implemented
- [x] Reciprocal Rank Fusion (RRF) for combining retrieval results
- [ ] PostgreSQL/pgvector vector storage and retrieval integration

**Current implementation note:** The existing retrieval pipeline uses FAISS and BM25 with RRF. PostgreSQL/pgvector is available through Docker Compose, but vector storage and retrieval integration with pgvector is still pending.

## Future Dataset Expansion

The future dataset target is:

- At least 18 annual reports across three reporting years.
- More than 6,000 PDF pages.
- Relevant Business Responsibility and Sustainability Reports (BRSR).
- Improved year-wise comparison of rural FMCG strategies.
