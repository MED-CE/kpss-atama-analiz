# KPSS Merkezi Atama Analiz Platformu

Türkiye'deki KPSS merkezi atamalarını 2010 yılından günümüze kadar resmi kaynaklardan (ÖSYM) toplayan ve analiz eden sistem.

## Architecture

- **Frontend:** Next.js (SSR, Tailwind CSS, shadcn/ui) - Deployed on Azure Static Web Apps
- **Backend:** FastAPI (Python, SQLAlchemy) - Deployed on Azure Functions (Serverless)
- **Database:** PostgreSQL - Appwrite Education Plan
- **Storage:** Azure Blob Storage for raw PDFs and Excel files
- **Scraper / Worker:** GitHub Actions (Weekly schedule)
- **Monitoring:** Sentry

## MONTHLY COST (Target: $0)

| Service | Expected Cost | Notes |
|---|---|---|
| Frontend | $0 | Azure Static Web Apps Free Tier / GitHub Pages |
| Backend | $0 | Azure Functions (1M free execs/mo) |
| Database | $0 | Appwrite Education ($10 credit covers base Postgres) |
| Storage | $0 | Azure Blob Storage (5GB Free for Students) |
| Scraper | $0 | GitHub Actions (2000 mins/mo free) |
| OCR | $0 | GitHub Actions CPU (Tesseract) |
| Monitoring | $0 | Sentry Student Pack (500k events/mo) |
| CI/CD | $0 | GitHub Actions |

**Total:** $0/mo

## Rules & Development

- No local services are used for production.
- Do not commit `.env` files or secrets.
- Data sources must be labeled as `OFFICIAL` (ÖSYM) or `THIRD_PARTY`.
- Use Codespaces for development.
