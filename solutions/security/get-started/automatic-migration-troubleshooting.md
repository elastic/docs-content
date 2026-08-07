---
navigation_title: "No integrations for translated rules"
description: "Fix missing integrations for translated rules in Automatic Migration, caused by the elser_embedding field being bound to the wrong inference endpoint."
type: troubleshooting
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

# No integrations shown for translated rules

After an Automatic Migration completes, the **Integrations** column on the **Translated rules** page can show no integrations, even when matching integrations exist. This page helps you confirm whether the cause is a misconfigured inference endpoint, and how to fix it.

## Symptoms

- The **Integrations** column on the **Translated rules** page shows no integrations for rules that have a matching integration.
- Semantic search results based on the affected index are inconsistent or empty.

## Diagnosis

Integration matching relies on semantic search against the `.kibana-siem-rule-migrations-integrations` index, which stores a `semantic_text` field named `elser_embedding`. That field is intended to use Elastic's ELSER sparse embedding model, but on some deployments it can be bound to a different embedding model instead—for example, a Jina dense embedding model with `inference_id: .jina-embeddings-v5-text-small`.

This typically happens because the ELSER inference endpoint wasn't available yet when the index was created, so {{es}} fell back to whichever inference endpoint was configured at the time. The field name `elser_embedding` is only a label—what determines the model actually used is the `inference_id` baked into the index mapping at creation time.

To confirm this is the cause, run the following requests in the {{kib}} [Dev Tools Console](/explore-analyze/query-filter/tools/console.md):

1. Check which inference endpoints exist on the cluster:

   ```http
   GET _inference
   ```

   If you only see Jina or other non-ELSER endpoints, ELSER hasn't been deployed on this cluster. Create it in [Step 1](#create-elser-endpoint) of the resolution.

2. Check the `inference_id` for the `elser_embedding` field:

   ```http
   GET .kibana-siem-rule-migrations-integrations/_mapping/field/elser_embedding
   ```

   If `inference_id` shows `.jina-embeddings-v5-text-small` (or anything other than an ELSER endpoint), the field is misconfigured and the resolution below applies. For example:

   ```json
   "elser_embedding": {
     "type": "semantic_text",
     "inference_id": ".jina-embeddings-v5-text-small"
   }
   ```

   A correctly configured mapping references an ELSER inference endpoint instead, for example:

   ```json
   "elser_embedding": {
     "type": "semantic_text",
     "inference_id": "elser-2-elasticsearch"
   }
   ```

## Resolution

Recreate the index with the correct ELSER inference endpoint, then reindex all documents so their embeddings are regenerated using ELSER.

Before you start:

- Confirm ELSER is available on your cluster, or be prepared to create it in Step 1.
- You need index admin privileges.
- Make sure no automatic migrations are running. If one is running, stop it before you continue.

::::{warning}
This resolution deletes and recreates a {{kib}} system index directly through {{es}} APIs. Take a cluster snapshot before you begin, and contact [Elastic support](/troubleshoot/index.md#contact-us) if you're unsure about any step.
::::

:::::{stepper}

::::{step} Create the ELSER inference endpoint
:anchor: create-elser-endpoint

Skip this step if [Diagnosis](#diagnosis) confirmed ELSER is already deployed.

Create the endpoint with the following request, or deploy ELSER from the {{kib}} **Model Management** → **Trained Models** page. For more information, refer to [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md).

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

This registers a new ELSER sparse embedding inference endpoint with the ID `elser-2-elasticsearch`, which the following steps reference in the index mapping. If you deploy ELSER from {{kib}} instead, use that endpoint ID in the mapping examples below.

:::{note}
The inference ID can't start with a dot (`.`)—that prefix is reserved for system-provisioned endpoints on {{ecloud}}. Use a plain alphanumeric name.

Adjust the adaptive allocation settings and `num_threads` for better throughput during reindex if your cluster has spare {{ml}} capacity.
:::

::::

::::{step} Create a backup index

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

:::{note}
**Why `dynamic: false`:** ELSER sparse vectors store thousands of unique NLP tokens as sub-fields at index time. With `dynamic: true` (the default), each token becomes a new mapped field, quickly exhausting `total_fields.limit`. Setting `dynamic: false` keeps those token fields out of the mapping while still allowing them to be indexed and searched correctly.

**Why a backup index first:** The `inference_id` of a `semantic_text` field can't be changed in place—its mapping is immutable. Reindexing into a separate backup index first lets you validate the result before you delete the original, and it remains available as a backup after final verification.
:::

::::

::::{step} Reindex into the backup index

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

This copies the original documents into the backup index, which uses the corrected `elser_embedding` mapping, so their embeddings are regenerated with the new ELSER inference endpoint.

`wait_for_completion=false` returns a task ID immediately so the reindex runs in the background. Use that task ID in the next step to monitor progress.

::::

::::{step} Monitor the reindex task

```http
GET _tasks/<task_id>
```

Replace `<task_id>` with the one returned in the previous step. Check for:

- `"completed": true`—reindex finished.
- `"failures": []`—no documents failed.
- `response.created` equals `response.total`.

::::

::::{step} Verify document counts match

```http
GET .kibana-siem-rule-migrations-integrations/_count
GET kibana-siem-rule-migrations-integrations-backup/_count
```

Both counts must be equal before you continue. If the backup index has fewer documents, check the task failures from the previous step before proceeding.

::::

::::{step} Delete the original index

```http
DELETE .kibana-siem-rule-migrations-integrations
```

:::{warning}
This is irreversible. Only proceed if the previous two steps confirmed matching counts and zero failures.

{{kib}} SIEM rule migration features that depend on this index are unavailable until you recreate it in the next step.
:::

::::

::::{step} Recreate the original index with the correct mapping

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

The index name is hardcoded in {{kib}}'s SIEM rule migration code, so it must exist under its original name. This recreates it using the same corrected mapping as the backup index.

::::

::::{step} Reindex from the backup index back into the original

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

::::

::::{step} Monitor the second reindex task

```http
GET _tasks/<task_id>
```

Replace `<task_id>` with the one returned in the previous step, and apply the same checks as when you monitored the first reindex.

::::

::::{step} Confirm the fix

```http
GET .kibana-siem-rule-migrations-integrations/_count
GET kibana-siem-rule-migrations-integrations-backup/_count
GET .kibana-siem-rule-migrations-integrations/_mapping/field/elser_embedding
```

Confirm that both document counts match, and that `inference_id` now shows `elser-2-elasticsearch`. Keep `kibana-siem-rule-migrations-integrations-backup` available as a backup after final verification.

::::

:::::

## Resources

- [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md)
- {{kib}} [Dev Tools Console](/explore-analyze/query-filter/tools/console.md)

:::{tip}
If you have an [Elastic subscription](https://www.elastic.co/pricing), you can [contact Elastic support](/troubleshoot/index.md#contact-us) for assistance.
:::
