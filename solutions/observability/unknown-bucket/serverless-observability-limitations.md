---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-limitations.html
---

# Serverless observability limitations [observability-limitations]

Currently, the maximum ingestion rate for the Managed Intake Service (APM and OpenTelemetry ingest) is 11.5 MB/s of uncompressed data (roughly 1TB/d uncompressed equivalent). Ingestion at a higher rate may experience rate limiting or ingest failures.

If you believe you are experiencing rate limiting or other ingest-based failures, please [contact Elastic Support](../../../troubleshoot/index.md) for assistance.

