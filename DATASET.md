
# ShelfSignal Dataset

## Project Overview

ShelfSignal collects annual reports from six FMCG companies to support research on rural growth, pricing, and business performance.

The reports are stored as PDF files in the `data/sample/` directory.

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

The dataset covers the following FMCG companies:

1. Hindustan Unilever Limited (HUL)
2. ITC Limited
3. Nestlé India
4. Dabur India
5. Marico Limited
6. Britannia Industries

## Dataset Inventory

| Company | Report | Total Pages | Pages with Text |
|---|---|---:|---:|
| Britannia | 2025-26 | 189 | 189 |
| Dabur | 2025-26 | 623 | 622 |
| HUL | 2025-26 | 244 | 244 |
| ITC | 2025-26 | 412 | 411 |
| Marico | 2025-26 | 279 | 279 |
| Nestle India | 2025-26 | 306 | 304 |

Total reports: 6
Total pages: 2053
Pages with extractable text: 2049

## Data Collection Notes

- Annual report PDFs from six FMCG companies are organized by company.
- Each report is stored in its respective company folder under `data/sample/`.
- The reporting year is included in each PDF filename.
- All six PDFs have been verified for page counts and text extraction.
- A total of 2,053 pages were identified, with extractable text available on 2,049 pages.
- PDF page counts and text extraction details are documented in the dataset inventory.
- The collected reports will be used as source documents for researching FMCG rural growth, sales performance, and pricing.

