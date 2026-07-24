---
navigation_title: Cloud token runtime failure
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Cloud token runtime failure [cps-datafeed-cloud-token-runtime-failure]

After {{cps}} credentials were minted successfully, the stored internal cloud API key can **later** fail authorization during periodic {{dfeeds}} searches. Cross-project portions of the search may be skipped or degraded while the {{dfeeds}} keeps running on whatever scope still succeeds.

If create or update fails immediately with a mint error, see [Cloud token mint failure](cps-datafeed-cloud-token-mint-failure.md) instead.

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Diagnose cloud token runtime failure [diagnose-cps-datafeed-cloud-token-runtime-failure]

**When it happens**

Runtime failure occurs **after** a successful create or update. The {{dfeeds}} holds a persisted internal credential but that key no longer authorizes cross-project search.

**Check the stored key id**

```console
GET _ml/datafeeds/{datafeed_id}
```

When an internal credential exists, the response includes `authorization.cloud_api_key.id` (never the raw credential envelope).

Verify key status:

```console
GET _security/api_key?id={authorization.cloud_api_key.id}
```

Look for `invalidated: true`, expiration, or a missing key.

**Review job Messages**

Open **ML → Anomaly Detection → your job → Messages** (or query `.ml-notifications-*`) for credential lifecycle entries such as:

```txt
Internal cloud API key minted for cross-project datafeed
```

```txt
Internal cloud API key re-keyed for cross-project datafeed update
```

A mint or re-key message followed by new extraction auth errors suggests the stored key is no longer valid at runtime.

**Rule out linked-project skips**

Auth failures can co-occur with project skips. Check `remote_cluster_stats` on stats and read the full extraction error — pure connectivity skips use a different root message:

```txt
[N] remote clusters out of [M] were skipped when performing datafeed search
```

See [Linked project skipped](cps-datafeed-linked-project-skipped.md) when skips dominate and the key is still valid.

## Resolve cloud token runtime failure [resolve-cps-datafeed-cloud-token-runtime-failure]

**Force re-key with a cloud-authenticated update**

Issue an update signed in as a valid {{ecloud}} user ({{kib}} session or cloud-managed API credential). Even a no-op config change triggers a fresh internal key:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "indices": ["<unchanged>"],
  "project_routing": "<unchanged or explicit current value>"
}
```

:::{important}
Use a cloud-authenticated caller. Stack API keys alone may clear the internal credential instead of re-keying it.
:::

**Verify recovery**

```console
GET _ml/datafeeds/{datafeed_id}
GET _security/api_key?id={new authorization.cloud_api_key.id}
GET _ml/datafeeds/{datafeed_id}/_stats
```

Expect a new `authorization.cloud_api_key.id`, `invalidated: false`, and restored linked-project search scope in `remote_cluster_stats`. **Messages** should record a re-key event.

**Escalate if re-key does not help**

If a cloud-authenticated re-key completes but cross-project search still fails authorization, contact Elastic support with:

- Origin project id
- {{dfeeds}} and job id
- `authorization.cloud_api_key.id` before and after re-key
- Relevant **Messages** excerpts
