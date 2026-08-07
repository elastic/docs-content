---
navigation_title: Credential problems
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Cloud credential problems [cps-datafeed-credentials]

A {{cps}} {{dfeed}} stores an internal cloud (UIAM) API key so periodic searches can read linked projects on your behalf. {{es}} mints that key only when a cloud-authenticated caller creates or updates the {{dfeed}}, not during a scheduled extraction cycle. Failures fall into four paths: the key could not be created, an existing key no longer authorizes search, the key was cleared by a non-cloud-authenticated update, or no key was ever minted because the {{dfeed}} was created or last updated without cloud authentication.

## Diagnose cloud credential problems [diagnose-cps-datafeed-credentials]

:::{include} /troubleshoot/_snippets/cps-ml-diagnostics-sources.md
:::

**Which failure is this?**

Use observable behavior to pick a path:

- **Create or update fails immediately**: Error during validation before minting or during minting itself. See **Creation and update failures** below.
- **Searches used to work and** `GET _ml/datafeeds/{datafeed_id}` **contains** `authorization.cloud_api_key.id`: runtime auth or authz failure. See **Runtime failures** below.
- `authorization.cloud_api_key.id` **is missing**: two cases:
  - **Credential cleared**: **Job messages** record `Internal cloud API key cleared on datafeed update with non-cloud credentials` after a non-cloud-authenticated update removed a stored key. See **Credential cleared** below.
  - **Never minted**: the {{dfeed}} was created or last updated without cloud authentication, so no key was ever stored and no CLEARED message appears. **Job messages** lack `Internal cloud API key minted for cross-project datafeed`. Mint a key with a cloud-authenticated create or update.

**Creation and update failures**

{{es}} runs a validate-before-mint search probe with the caller's credential before storing a new internal key. Probe failures fail the create or update synchronously.

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

The bracketed status is the `RestStatus` enum name (for example `UNAUTHORIZED` or `FORBIDDEN`), not an HTTP status code.

Routing that matches no linked project is reported separately. See [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md).

**Runtime failures**

After minting succeeds, periodic searches can fail when the stored credential is invalid or lacks privileges. **Job messages** record:

Invalidated or expired key:

```txt
Internal cloud API key [abc123def456] failed authentication during datafeed search; it may have been revoked or expired. Re-key by issuing a cloud-authenticated POST _ml/datafeeds/_update on this datafeed
```

The bracketed value is the key **identifier** (the same `authorization.cloud_api_key.id` from `GET _ml/datafeeds/{datafeed_id}`), not the credential secret. {{es}} never logs or returns the internal key text.

Insufficient privileges:

```txt
Datafeed search was denied (forbidden) while using internal cloud API key [abc123def456]; the key's privileges or the requesting user's cross-project access may be insufficient. Verify the key and the datafeed owner's project privileges, then re-key with a cloud-authenticated update if the key is the cause
```

**Credential cleared**

When a caller that is **not** cloud-authenticated updates a {{dfeed}} that still has a stored internal key, {{es}} clears the credential instead of re-keying it. **Job messages** record:

```txt
Internal cloud API key cleared on datafeed update with non-cloud credentials
```

After clearing, `GET _ml/datafeeds/{datafeed_id}` omits `authorization.cloud_api_key.id`. Cross-project portions of the search fail until a cloud-authenticated update mints a new key.

**Lifecycle messages for context**

Success entries for timeline context (not failure signals):

```txt
Internal cloud API key minted for cross-project datafeed
```

```txt
Internal cloud API key re-keyed for cross-project datafeed update
```

```txt
Internal cloud API key revoked for cross-project datafeed
```

```txt
Skipping revocation of cloud API key [abc123def456] — revoke primitive not yet available
```

A mint or re-key followed by a runtime failure means the key worked at create or update time but later stopped authorizing search.

## Resolve cloud credential problems [resolve-cps-datafeed-credentials]

:::{include} /troubleshoot/_snippets/cps-ml-update-preconditions.md
:::

**Re-create or re-key the credential**

Resolve missing index privileges, routing that matches nothing, or other validate-before-mint errors before retrying create or update. Sign in to {{kib}} or call the API as a cloud-authenticated user: a {{ecloud}} session or cloud-managed credential, not a stack API key alone.

When a stored key still exists but no longer works, stop the {{dfeed}} and issue a force re-key:

```console
POST _ml/datafeeds/my-datafeed/_update
{
  "_force_rekeying": true
}
```

Replace `my-datafeed` with your {{dfeed}} id. Expect `Internal cloud API key re-keyed for cross-project datafeed update` in **Job messages** and a new `authorization.cloud_api_key.id` on `GET _ml/datafeeds/{datafeed_id}`.

{{es}} also re-keys automatically when a cloud-authenticated update changes the cross-project search surface: `project_routing`, `indices`, or `indices_options`. A no-op update without `_force_rekeying` does not replace an existing key.

When the credential was cleared, a cloud-authenticated update mints a new key even if the configuration is unchanged.

**Avoid clearing the credential**

Use {{kib}} signed in to {{ecloud}} or an API client with cloud-managed authentication. Non-cloud-authenticated callers clear the internal key instead of minting or re-keying it. `_force_rekeying` requires cloud authentication; operator basic-auth updates return a validation error.

**Verify recovery**

```console
GET _ml/datafeeds/{datafeed_id}
GET _ml/datafeeds/{datafeed_id}/_stats
```

Expect a new `authorization.cloud_api_key.id`, a mint or re-key entry in **Job messages**, and successful extraction cycles in `_stats` once linked projects authorize search again.

**Escalation**

If a cloud-authenticated force re-key or surface-changing update completes but cross-project search still fails, contact [Elastic support](/troubleshoot/index.md#contact-us) with:

- Origin project id
- {{anomaly-job}} and {{dfeed}} ids
- `authorization.cloud_api_key.id` before and after the update
- Relevant **Job messages** excerpts (probe errors, runtime failures, or lifecycle entries)

**Superseded key revocation**

After re-keying, {{es}} best-effort revokes the old key. If revocation fails:

```txt
Failed to revoke internal cloud API key [abc123def456]
```

Search uses the new key. The message is informational and does not block recovery.
