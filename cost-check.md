# Deployment Cost Guard

Before any production deployment, verify the following constraints to maintain the $0 cost target:

## 1. Services & SKUs
- **Frontend (Azure Static Web Apps)**: Must be `Free` tier.
- **Backend (Azure Functions)**: Must be `Consumption` plan (Serverless). Check that we do not exceed 1M executions.
- **Database (Appwrite Postgres)**: Ensure it runs under the Student $10 monthly credit limit.
- **Storage (Azure Blob Storage)**: Must use `Standard_LRS` (Locally Redundant Storage), limit to 5GB.
- **Sentry**: Verify it uses the GitHub Student Pack free limits.

## 2. Limits & Quotas
- Monitor GitHub Actions minute usage (Limit: 2,000 mins/month for private repos, though public is free).
- If Azure Student credits ($100) are consumed, verify that "Always Free" services remain free without automatic paid fallback.

## 3. Alerts
- Budget Alert must be set in Azure for $1.00 to prevent unexpected charges.
- Never authorize "Pay-as-you-go" credit card billing without explicit user approval.
