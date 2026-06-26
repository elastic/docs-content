---
applies_to:
  stack: preview =9.0, ga 9.1+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Troubleshoot Automatic Migration

## Wrong inference model on the `elser_embedding` field

### Problem description

The `.kibana-siem-rule-migrations-integrations` index contains a `semantic_text` field named `elser_embedding` that is intended to use Elastic's ELSER sparse embedding model for semantic search. However, on some deployments the field may be bound to a different embedding model (for example, a Jina dense embedding model with `inference_id: .jina-embeddings-v5-text-small`) instead.

This causes the following symptoms:

- **Inconsistent search results across machines or clusters** — the same query returns different documents because the query-time inference model doesn't match the index-time model on the other cluster.
- **Semantic search returning no results or wrong results** — Jina produces dense vectors; ELSER produces sparse vectors; they are incompatible vector spaces.
- **`function_score` queries with `min_score` returning zero hits** — scores computed against mismatched embeddings are meaningless and rarely cross any threshold.

The root cause is that when the index was created, the ELSER inference endpoint was not available, so Elasticsearch fell back to whichever inference endpoint was configured. The field name `elser_embedding` is just a label; what matters is the `inference_id` baked into the index mapping at creation time.

The fix requires re-creating the index with the correct ELSER inference endpoint and re-indexing all documents so their embeddings are regenerated using ELSER.

### Prerequisites

- ELSER ML model must be available and startable on the cluster.
- You must have index admin privileges.
- Expect downtime or degraded search on this index during the reindex process.

---

### Step 1 — Verify the problem

**1a. Check what inference endpoints are currently configured on the cluster:**

```http
GET _inference
```

Confirm whether an ELSER endpoint exists. If you only see Jina or other non-ELSER endpoints, ELSER has not been deployed on this cluster and must be created in Step 2.

**1b. Check what `inference_id` is bound to the `elser_embedding` field:**

```http
GET .kibana-siem-rule-migrations-integrations/_mapping/field/elser_embedding
```

Look for the `inference_id` inside the field mapping. If it shows `.jina-embeddings-v5-text-small` (or anything other than an ELSER endpoint), the field is misconfigured and the steps below are required.

---

### Step 2 — Create the ELSER inference endpoint

```http
PUT _inference/sparse_embedding/elser-2-elasticsearch
{
  "service": "elser",
  "service_settings": { "num_allocations": 1, "num_threads": 1 }
}
```

This registers a new ELSER sparse embedding inference endpoint with the ID `elser-2-elasticsearch`. This ID will be referenced in the index mapping.

::::{note}
The inference ID cannot start with a dot (`.`) — that prefix is reserved for system-provisioned endpoints on Elastic Cloud. Use a plain alphanumeric name.

Increase `num_allocations` and `num_threads` for better throughput during reindex if your cluster has spare ML capacity.
::::

---

### Step 3 — Create a staging index (`-v2`)

```http
PUT .kibana-siem-rule-migrations-integrations-v2
{
  "settings": {
    "index.mapping.total_fields.limit": 2000
  },
  "mappings": {
    "dynamic": false,
    "properties": {
      "id": { "type": "keyword" },
      "title": { "type": "text" },
      "description": { "type": "text" },
      "data_streams": {
        "type": "object",
        "properties": {
          "title": { "type": "text" },
          "dataset": { "type": "keyword" },
          "index_pattern": { "type": "keyword" }
        }
      },
      "elser_embedding": {
        "type": "semantic_text",
        "inference_id": "elser-2-elasticsearch"
      }
    }
  }
}
```

::::{note}
**Why `dynamic: false`:** ELSER sparse vectors store thousands of unique NLP tokens as sub-fields at index time. With `dynamic: true` (the default), each token becomes a new mapped field, quickly exhausting the `total_fields.limit`. Setting `dynamic: false` prevents these token fields from being added to the mapping while still allowing them to be indexed and searched correctly.

**Why a staging index (`-v2`) first:** The original index cannot have its `inference_id` changed in-place — mappings are immutable for `semantic_text` fields. A staging index lets you validate the reindex succeeded before destroying the original.
::::

---

### Step 4 — Reindex into the staging index

```http
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": ".kibana-siem-rule-migrations-integrations",
    "_source": {
      "excludes": ["elser_embedding"]
    }
  },
  "dest": {
    "index": ".kibana-siem-rule-migrations-integrations-v2"
  },
  "script": {
    "source": """
      def embedding = ctx._source.remove('elser_embedding');
      if (embedding != null) {
        if (embedding instanceof Map && embedding.containsKey('text')) {
          ctx._source['elser_embedding'] = embedding['text'];
        } else if (embedding instanceof String) {
          ctx._source['elser_embedding'] = embedding;
        }
      }
    """,
    "lang": "painless"
  }
}
```

::::{note}
**Why `excludes: ["elser_embedding"]`:** The source documents contain vector data stored inside the `elser_embedding` field structure. Excluding it from `_source` prevents the raw vector payload from being copied. The Painless script then re-injects only the plain text back into `elser_embedding`, which triggers the new ELSER inference endpoint to generate fresh sparse embeddings on ingest.

**`wait_for_completion=false`:** Returns a task ID immediately so the reindex runs in the background. Use the task ID in Step 5 to monitor progress.
::::

---

### Step 5 — Monitor the reindex task

```http
GET _tasks/<task_id>
```

Replace `<task_id>` with the one returned in Step 4.

Check for:
- `"completed": true` — reindex finished.
- `"failures": []` — no documents failed.
- `response.created` should equal `response.total`.

---

### Step 6 — Verify document counts match

```http
GET .kibana-siem-rule-migrations-integrations/_count
GET .kibana-siem-rule-migrations-integrations-v2/_count
```

Both counts must be equal before proceeding. If the staging index (`-v2`) has fewer documents, check the task failures from Step 5 before continuing.

---

### Step 7 — Delete the original index

```http
DELETE .kibana-siem-rule-migrations-integrations
```

::::{warning}
This is irreversible. Only proceed if Step 6 confirmed counts match and Step 5 showed zero failures.

Kibana SIEM rule migration features that depend on this index will be unavailable until Step 9 completes.
::::

---

### Step 8 — Recreate the original index with the correct mapping

```http
PUT .kibana-siem-rule-migrations-integrations
{
  "settings": {
    "index.mapping.total_fields.limit": 2000
  },
  "mappings": {
    "dynamic": false,
    "properties": {
      "id": { "type": "keyword" },
      "title": { "type": "text" },
      "description": { "type": "text" },
      "data_streams": {
        "type": "object",
        "properties": {
          "title": { "type": "text" },
          "dataset": { "type": "keyword" },
          "index_pattern": { "type": "keyword" }
        }
      },
      "elser_embedding": {
        "type": "semantic_text",
        "inference_id": "elser-2-elasticsearch"
      }
    }
  }
}
```

The original index name is hardcoded in Kibana's SIEM rule migration code. The index must exist under its original name. This step recreates it with the correct mapping used for the staging index.

---

### Step 9 — Reindex from the staging index back into the original

```http
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": ".kibana-siem-rule-migrations-integrations-v2"
  },
  "dest": {
    "index": ".kibana-siem-rule-migrations-integrations"
  }
}
```

The staging index already contains correct ELSER embeddings, so no script or exclusions are needed — this is a straight document copy.

---

### Step 10 — Monitor the second reindex task

```http
GET _tasks/<task_id>
```

Replace `<task_id>` with the one returned in Step 9. Apply the same checks as Step 5.

---

### Step 11 — Final verification

```http
GET .kibana-siem-rule-migrations-integrations/_count
GET .kibana-siem-rule-migrations-integrations-v2/_count
```

Confirm that both document counts match.

---

### Step 12 — Clean up the staging index

```http
DELETE .kibana-siem-rule-migrations-integrations-v2
```

Only delete once Step 11 confirms counts match. Keep the staging index as a backup until you are confident the original is working correctly.

---

### Step 13 — Confirm the fix

```http
GET .kibana-siem-rule-migrations-integrations/_mapping/field/elser_embedding
```

The `inference_id` should now show `elser-2-elasticsearch`. If it does, the field is correctly bound to ELSER and semantic search queries will produce consistent, correct results.

---

### Summary of root causes addressed

| Problem | Cause | Fix applied |
|---|---|---|
| Wrong inference model on `elser_embedding` | Index created when ELSER was unavailable; fell back to a different model | Recreated index with explicit `inference_id: elser-2-elasticsearch` |
| Inconsistent results across machines | Different vector spaces (dense vs ELSER sparse) | All embeddings regenerated with ELSER |
| `total_fields.limit` exceeded during reindex | ELSER tokens dynamically mapped as individual fields | Set `dynamic: false` on index mapping |
| Old vectors copied instead of re-embedded | `elser_embedding` source contained vector structure | Excluded field from `_source`, re-injected plain text via Painless script |
