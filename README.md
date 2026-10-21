# Rural FMCG Insights

## Problem Understanding

FMCG companies publish annual reports and BRSRs containing information about rural demand, pricing strategies, new product launches, and market growth. However, these reports are often hundreds of pages long, making them difficult to access on budget smartphones with slow internet connections.

Sales officers at FMCG distributors need quick, relevant information from these reports to understand company strategies and make better rural stock-planning decisions.

## Proposed Solution

Build a mobile-friendly assistant that helps users ask questions about FMCG company reports and receive short, relevant answers without reading entire PDFs.

The system retrieves relevant information from reports and provides concise answers with source references while minimizing data usage and loading time.

## Report Coverage

The project will cover six FMCG companies over three years:

- Hindustan Unilever Limited (HUL)
- ITC Limited
- Nestlé India
- Dabur India
- Marico
- Britannia Industries

**Target:** At least 18 annual reports and 6,000+ pages, collected from official investor and company websites, along with relevant BRSR documents.

## Key Focus Areas

- Rural market demand and growth
- Pricing changes and product affordability
- New product launches and smaller pack sizes
- Distribution expansion and rural market reach
- Comparison of company strategies across three years

## Tech Stack

- **Programming Language:** Python
- **PDF Processing:** PyMuPDF
- **Text Embeddings:** Sentence Transformers
- **Vector Database:** FAISS
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Database:** SQLite
- **AI/LLM:** LLM-based question answering with Retrieval-Augmented Generation (RAG)

## Expected Outcome

A lightweight, mobile-friendly solution that converts large corporate reports into simple, source-backed answers, helping FMCG sales officers understand market trends and plan rural stock more effectively.