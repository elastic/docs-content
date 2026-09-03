---
navigation_title: Troubleshoot cloud credentials
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Troubleshoot cloud credential problems

A {{cps}} {{dfeed}} stores an internal cloud API key so periodic searches can read linked projects on your behalf. {{es}} mints that key only when a cloud-authenticated caller creates or updates the {{dfeed}}, not during a scheduled extraction cycle. Failures fall into three paths covered on this page: the key could not be created, an existing key no longer authorizes search, or the key was cleared or never minted.

## Where to look

:::{include} /troubleshoot/_snippets/cps-ml-diagnostics-sources.md
:::

## Creation or update failures

### What you see

{{es}} probes the search with the caller's credential before storing a new internal key. Probe failures fail the create or update synchronously.

Missing index privileges in a linked project:

```txt
User lacks the required permissions to read datafeed indices on project [...].
```

On a specific index in the origin project or a qualified index pattern:

```txt
User lacks the required permissions to read datafeed index [...].
```

The bracketed project alias or index name varies. When no single index is named:

```txt
User lacks the required permissions to read from the datafeed indices.
```

Other probe failures surface as:

```txt
Datafeed search probe failed with status [FORBIDDEN]
```

The bracket shows a status name such as `UNAUTHORIZED` or `FORBIDDEN`, not an HTTP status code.

Routing that matches no linked project is reported separately. See [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md).

### Fix

Resolve missing index privileges, routing that matches nothing, or other probe errors before retrying create or update. Sign in to {{kib}} or call the API as a cloud-authenticated user: a {{ecloud}} session or cloud-managed credential, not a stack API key alone.

Use {{kib}} signed in to {{ecloud}} or an API client with cloud-managed authentication. Non-cloud-authenticated callers clear the internal key instead of minting or re-keying it.

### Verify

The create or update succeeds. Job messages show `Internal cloud API key minted for cross-project datafeed`. `GET _ml/datafeeds/{datafeed_id}` includes `authorization.cloud_api_key.id`.

## Runtime authorization failures

### What you see

After minting succeeds, periodic searches can fail when the stored credential is invalid or lacks privileges. Job messages record:

Invalidated or expired key:

```txt
Internal cloud API key [abc123def456] failed authentication during datafeed search; it may have been revoked or expired. Re-key by issuing a cloud-authenticated POST _ml/datafeeds/_update on this datafeed
```

The bracketed value is the key **identifier** (the same `authorization.cloud_api_key.id` from `GET _ml/datafeeds/{datafeed_id}`), not the credential secret. {{es}} never logs or returns the internal key text.

Insufficient privileges:

```txt
Datafeed search was denied (forbidden) while using internal cloud API key [abc123def456]; the key's privileges or the requesting user's cross-project access may be insufficient. Verify the key and the datafeed owner's project privileges, then re-key with a cloud-authenticated update if the key is the cause
```

A mint or re-key followed by a runtime failure means the key worked at create or update time but later stopped authorizing search.

### Fix

Stop the {{dfeed}} and issue a force re-key:

```console
POST _ml/datafeeds/my-datafeed/_update
{
  "_force_rekeying": true
}
```

Replace `my-datafeed` with your {{dfeed}} id. `_force_rekeying` requires cloud authentication; operator basic-auth updates return a validation error.

{{es}} also re-keys automatically when a cloud-authenticated update changes the cross-project search surface: `project_routing`, `indices`, or `indices_options`. A no-op update without `_force_rekeying` does not replace an existing key.

### Verify

```console
GET _ml/datafeeds/{datafeed_id}
GET _ml/datafeeds/{datafeed_id}/_stats
```

Expect a new `authorization.cloud_api_key.id`, a re-key entry in job messages, and successful extraction cycles in `_stats` once linked projects authorize search again.

After re-keying, {{es}} best-effort revokes the old key. If revocation fails, job messages might show `Failed to revoke internal cloud API key [abc123def456]`. Search uses the new key. The message is informational and does not block recovery.

## Cleared or never-minted credential

### What you see

When `authorization.cloud_api_key.id` is missing, distinguish two cases:

* **Credential cleared**: job messages record `Internal cloud API key cleared on datafeed update with non-cloud credentials` after a non-cloud-authenticated update removed a stored key.
* **Never minted**: the {{dfeed}} was created or last updated without cloud authentication, so no key was ever stored and no CLEARED message appears. Job messages lack `Internal cloud API key minted for cross-project datafeed`.

When a caller that is **not** cloud-authenticated updates a {{dfeed}} that still has a stored internal key, {{es}} clears the credential instead of re-keying it:

```txt
Internal cloud API key cleared on datafeed update with non-cloud credentials
```

After clearing, `GET _ml/datafeeds/{datafeed_id}` omits `authorization.cloud_api_key.id`. Cross-project portions of the search fail until a cloud-authenticated update mints a new key.

### Fix

Issue a cloud-authenticated update. When the credential was cleared, a cloud-authenticated update mints a new key even if the configuration is unchanged.

### Verify

`GET _ml/datafeeds/{datafeed_id}` includes a new `authorization.cloud_api_key.id`. Job messages show `Internal cloud API key minted for cross-project datafeed` or `Internal cloud API key re-keyed for cross-project datafeed update`.

### When to contact support

If a cloud-authenticated force re-key or surface-changing update completes but cross-project search still fails, contact [Elastic support](/troubleshoot/index.md#contact-us) with:

* Origin project id
* {{anomaly-job}} and {{dfeed}} ids
* `authorization.cloud_api_key.id` before and after the update
* Relevant job message excerpts (probe errors, runtime failures, or lifecycle entries)
