---
navigation_title: Cloud token mint failure
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Cloud token mint failure [cps-datafeed-cloud-token-mint-failure]

{{cps}} {{ml}} {{dfeeds}} mint an internal cloud API key when you **create** or **update** a datafeed (`PUT _ml/datafeeds/{id}` or `POST _ml/datafeeds/{id}/_update`). Mint failures happen at that moment — during the synchronous validate-before-mint step — not during periodic datafeed runs.

If the datafeed was created successfully but later searches fail authorization, see [Cloud token runtime failure](cps-datafeed-cloud-token-runtime-failure.md) instead.

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Diagnose cloud token mint failure [diagnose-cps-datafeed-cloud-token-mint-failure]

**When it happens**

Mint failure occurs only on create or update. A running {{dfeeds}} that already has credentials does **not** hit this path during extraction cycles.

**Error messages**

The API returns a synchronous error on `PUT` or `POST _ml/datafeeds/{id}/_update`. Cluster logs include:

```txt
Failed to mint internal cloud API key for CPS datafeed
```

The log line includes the {{dfeeds}} id. The API error body carries the underlying cause (for example, the owning user no longer exists or validate-before-mint search probe failed).

**Check job status in {{kib}}**

When mint fails, the {{anomaly-jobs}} list may show an **API key error** indicator on the affected job. For cloud API key prerequisites, refer to [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md).

**Confirm this is not a runtime failure**

| Mint failure (this page) | Runtime failure |
|--------------------------|-----------------|
| Fails on `PUT` / `POST _update` | {{dfeeds}} was persisted; periodic searches degrade |
| No successful credential lifecycle message yet | Prior messages such as `Internal cloud API key minted for cross-project datafeed` |
| Immediate API `4xx` response | Skipped linked projects or auth errors during extraction |

## Resolve cloud token mint failure [resolve-cps-datafeed-cloud-token-mint-failure]

**Re-establish ownership under a valid user**

Mint uses the user principal stored on the job. If that account was deleted or cannot receive a grant:

1. Sign in to {{kib}} as a **currently valid** user with rights to manage the job.
2. **Update** the {{dfeeds}} (or recreate the job) so credential mint runs under your account:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "indices": ["<unchanged>"],
  "project_routing": "<unchanged or intended value>"
}
```

3. Confirm the API key error indicator clears in the {{anomaly-jobs}} list.

**What does not fix mint failure**

Rotating your personal API key alone does **not** re-mint the job's internal cloud key. You must update or recreate the {{dfeeds}} while authenticated as a valid cloud user.

**Fix validate-before-mint probe errors**

If the error references search authorization or a missing project reference, fix `project_routing`, index qualifiers, or project links first, then retry the update. See [Linked project skipped](cps-datafeed-linked-project-skipped.md) and [Stale project reference](cps-datafeed-stale-project-reference.md).

If mint still fails after these steps, contact Elastic support with the {{dfeeds}} id and the full API error response.
