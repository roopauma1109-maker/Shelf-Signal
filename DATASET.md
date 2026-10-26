
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

## Data Collection Notes

- Annual report PDFs are organized by company.
- Each report is stored in its respective company folder.
- The reporting year is included in each PDF filename.
- PDF page counts and text extraction details will be documented separately after verification.
- The collected reports will be used as source documents for researching FMCG rural growth and pricing.

