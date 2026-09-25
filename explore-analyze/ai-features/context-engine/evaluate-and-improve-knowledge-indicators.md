---
navigation_title: "Evaluate and improve KIs"
description: Inspect Knowledge Indicator content, provenance, freshness, and retrieval behavior, then refine the automation that generates it.
type: how-to
applies_to:
  stack: experimental 9.6
  serverless: experimental
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# Evaluate and improve Knowledge Indicators

:::{include} _snippets/hidden-docs-notice.md
:::

A useful Knowledge Indicator (KI) gives an agent accurate, relevant context without making it rediscover the same information from raw data. Inspect KIs after an automation runs and whenever the source data or intended use changes. When a generated KI needs improvement, refine its source or automation so later runs produce the improvement consistently.

## Before you begin

You need an AI index that contains at least one generated KI. To create one and review the required access, follow [Get started with Context Engine](quickstart.md).

You can inspect and test KIs in a [managed AI index](concepts.md#managed-ai-indices), but you cannot refine its sources or automations. The owning Elastic integration maintains that configuration.

## Open a Knowledge Indicator

1. Find **Context** in the navigation menu or use the global search field.
2. Open the AI index you want to inspect.
3. Select the **Knowledge Indicators** tab.
4. If the AI index contains several KI types, filter the list by type.
5. Select a KI to expand its JSON document.

## Review the KI document

The following fields help you determine what a KI represents, where it came from, and how an agent can use it:

| Field | What to review |
|---|---|
| `id` | The KI's logical identity. An automation can reuse the ID to update the same KI on later runs. |
| `type` | What the KI represents, such as `index_metadata`, `document`, or `detection`. A type classifies the result. It is not the automation's generation strategy. |
| `title` and `description` | Whether an agent can identify the subject and intended use of the KI before reading its full content. |
| `content` | The knowledge the automation generated, including its meaning, findings, limitations, or usage guidance. |
| `tags` | Terms an agent can use to narrow retrieval to relevant KIs. |
| `attributes` | Structured values associated with the KI, such as verified {{esql}} queries or use-case-specific metadata. |
| `references` | Related source material or other resources and how each reference relates to the KI. |
| `expires_at` | An optional expiration timestamp. Confirm that it matches the useful lifetime of the content. |
| `@timestamp` and `updated_at` | When the KI was created and most recently updated. |
| `governance.provenance` | The Workflow, Workflow version, run, and space that created or most recently updated the KI. |

For example, a KI derived from support cases might look like this:

```json
{
  "id": "ki-support-feed-compaction-hot-tier",
  "type": "support.recurring_issue",
  "title": "Feed compaction stalls on the hot tier above 1,000 shards",
  "description": "A recurring cause of ingest backpressure in the reviewed cases.",
  "content": "The affected cases show a rising bulk rejection rate before compaction stalls.",
  "tags": ["tier:hot", "area:ingest"],
  "attributes": {
    "case_count": 14
  },
  "references": [
    {
      "uri": "index://support-cases",
      "relation": "derived_from",
      "description": "The support cases analyzed by the automation"
    }
  ],
  "expires_at": "2026-12-10T00:00:00Z",
  "governance": {
    "provenance": {
      "created_by": {
        "uri": "workflow://support-case-distiller",
        "metadata": {
          "version": 3,
          "run_id": "<workflow-run-id>"
        }
      }
    }
  }
}
```

KI types are free-form values. Use names that consistently identify what the documents represent. The generation strategy is a separate choice that controls which source records become KIs and how much information each KI contains. Refer to [Select a generation strategy](build-and-maintain-ai-index.md#select-a-generation-strategy) for common strategies.

## Evaluate the generated context

Review the KI as context for an agent, not only as a valid document. Confirm that it:

- Answers a recurring question or helps an agent decide what to query next.
- Adds business meaning, derived findings, or usage guidance that a mapping alone cannot provide.
- Distinguishes facts derived from the complete dataset from observations based on a sample.
- States important limitations, missing data, and the questions it cannot answer.
- Includes references or verified query patterns when an agent might need current details.
- Contains enough information to be useful without repeating an entire source document.

Syntax and runtime verification show that a generated query parses and runs. They do not prove that its fields, grouping, and calculations answer the intended question. Review the query logic and its results before relying on it as guidance for an agent.

## Check refresh behavior

1. Record the KI's `id`, `updated_at`, and provenance run ID.
2. Run its automation again.
3. Return to the **Knowledge Indicators** tab and open the KI.
4. Confirm that the automation updated the KI with the same `id` instead of creating an unintended duplicate.
5. Confirm that `updated_at`, provenance, and any source-dependent content reflect the latest run.

If the automation intentionally creates one KI per event or source document, multiple KIs are expected. Stable IDs are most important when an automation maintains one KI for a dataset, entity, or other long-lived subject.

## Test how an agent uses the KI

After you make the AI index available to an {{agent-builder}} agent:

1. Ask a question the KI can answer from its generated content.
2. Ask a question that requires current details from the source.
3. Inspect the reasoning and tool calls shown with each response. If trace collection is available, you can also [view the trace for the conversation round](/explore-analyze/ai-features/agent-builder/chat.md#view-traces).
4. Confirm that the agent retrieves the relevant KI, answers from it when appropriate, and queries the source only when it needs additional detail.

This test shows whether the KI reduces repeated source exploration. If the agent ignores the KI, retrieves an unrelated KI, or still performs broad source exploration, revise the AI index description, KI content and tags, source selection, or automation instructions.

Compare traces for repeated or related questions. Look for broad source searches or repeated sequences of tool calls that better KI content or query guidance can avoid. These patterns show where moving recurring interpretation into the automation can save time and model tokens on later questions.

## Improve the automation

Do not rely on one-off edits to a generated KI. Update the source or automation so future runs reproduce the correction. Depending on what you find:

- Refine the source when it omits relevant data or includes unrelated data.
- Refine the automation instructions when the KI lacks meaning, boundaries, or useful retrieval guidance.
- Select a different generation strategy when each KI represents too much or too little source material.
- Adjust the schedule or expiration time when the KI becomes stale before its next refresh.
- Add verification when a generated query or structured attribute can be checked automatically.

Run the automation again, then repeat the content, refresh, and retrieval checks until the KI supports its intended questions. Treat this as a feedback loop: agent use exposes gaps, automation changes address them, and later runs regenerate the context with those improvements.
