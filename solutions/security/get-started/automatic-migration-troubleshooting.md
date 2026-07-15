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

## No integrations found for translated rules (Wrong inference model on the `elser_embedding` field)

### Problem description

The `.kibana-siem-rule-migrations-integrations` index contains a `semantic_text` field named `elser_embedding` that is intended to use Elastic's ELSER sparse embedding model for semantic search. However, on some deployments the field might be bound to a different embedding model (for example, a Jina dense embedding model with `inference_id: .jina-embeddings-v5-text-small`) instead.

This can cause the following symptom:

- **No integrations found for translated rules** — after completing an automatic migration, the **Integrations** column on the Translated rules page shows no integrations even when they should exist, because integration matching relies on semantic search against this index.

The root cause is that when the index was created, the ELSER inference endpoint was not available, so Elasticsearch fell back to whichever inference endpoint was configured. The field name `elser_embedding` is a label, but what matters is the `inference_id` baked into the index mapping at creation time. To confirm whether the field is bound to the wrong inference endpoint, refer to [Check the `elser_embedding` inference ID](#verify-elser-inference-id).

The fix requires re-creating the index with the correct ELSER inference endpoint and re-indexing all documents so their embeddings are regenerated using ELSER.

### Prerequisites

- ELSER ML model must be available on the cluster.
- You must have index admin privileges.
- Expect downtime or degraded search on this index during the reindex process.

---

### Step 1 — Verify the problem

Run the following API requests in [Kibana Dev Tools Console](/explore-analyze/query-filter/tools/console.md).

**1a. Check what inference endpoints are currently configured on the cluster:**

```http
GET _inference
```

Confirm whether an ELSER endpoint exists. If you only see Jina or other non-ELSER endpoints, ELSER has not been deployed on this cluster and must be created in Step 2.

#### 1b. Check the elser_embedding inference ID [verify-elser-inference-id]

```http
GET .kibana-siem-rule-migrations-integrations/_mapping/field/elser_embedding
```

Look for the `inference_id` inside the field mapping. If it shows `.jina-embeddings-v5-text-small` (or anything other than an ELSER endpoint), the field is misconfigured and the remediation steps in this guide are required. For example:

```json
"elser_embedding": {
  "type": "semantic_text",
  "inference_id": ".jina-embeddings-v5-text-small"
}
```

The corrected mapping should reference an ELSER inference endpoint, such as:

```json
"elser_embedding": {
  "type": "semantic_text",
  "inference_id": "elser-2-elasticsearch"
}
```

---

### Step 2 — Create the ELSER inference endpoint

You can create the ELSER inference endpoint with the API request below, or deploy ELSER from the Kibana **Model Management** > **Trained Models** page. For more information, refer to [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md).

```http
PUT _inference/sparse_embedding/elser-2-elasticsearch
{
  "service": "elasticsearch",
  "service_settings": {
    "adaptive_allocations": {
      "enabled": true,
      "min_number_of_allocations": 1,
      "max_number_of_allocations": 10
    },
    "num_threads": 1,
    "model_id": ".elser_model_2"
  }
}
```

This registers a new ELSER sparse embedding inference endpoint with the ID `elser-2-elasticsearch`. This ID will be referenced in the index mapping. If you deploy ELSER from Kibana instead, use that endpoint ID in the mapping examples below.

::::{note}
The inference ID cannot start with a dot (`.`) — that prefix is reserved for system-provisioned endpoints on Elastic Cloud. Use a plain alphanumeric name.

Adjust the adaptive allocation settings and `num_threads` for better throughput during reindex if your cluster has spare ML capacity.
::::

---

### Step 3 — Create a backup index

```http
PUT kibana-siem-rule-migrations-integrations-backup
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

**Why a backup index first:** The original index cannot have its `inference_id` changed in-place — mappings are immutable for `semantic_text` fields. A backup index lets you validate the reindex succeeded before destroying the original, and it remains available after final verification.
::::

---

### Step 4 — Reindex into the backup index

```http
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": ".kibana-siem-rule-migrations-integrations"
  },
  "dest": {
    "index": "kibana-siem-rule-migrations-integrations-backup"
  }
}
```

::::{note}
**Why reindex into the backup index first:** The backup index uses the corrected `elser_embedding` mapping. Reindexing the original documents into this index applies the new ELSER inference endpoint before the original index is deleted and recreated.

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
GET kibana-siem-rule-migrations-integrations-backup/_count
```

Both counts must be equal before proceeding. If the backup index has fewer documents, check the task failures from Step 5 before continuing.

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

The original index name is hardcoded in Kibana's SIEM rule migration code. The index must exist under its original name. This step recreates it with the correct mapping used for the backup index.

---

### Step 9 — Reindex from the backup index back into the original

```http
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "kibana-siem-rule-migrations-integrations-backup"
  },
  "dest": {
    "index": ".kibana-siem-rule-migrations-integrations"
  }
}
```

The backup index already uses the corrected ELSER mapping, so this is a straight document copy back into the original index name.

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
GET kibana-siem-rule-migrations-integrations-backup/_count
```

Confirm that both document counts match.

---

### Step 12 — Confirm the fix

```http
GET .kibana-siem-rule-migrations-integrations/_mapping/field/elser_embedding
```

The `inference_id` should now show `elser-2-elasticsearch`. If it does, the field is correctly bound to ELSER. Keep `kibana-siem-rule-migrations-integrations-backup` available as a backup after final verification.

---
