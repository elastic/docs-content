---
navigation_title: Manage data quality
applies_to:
  serverless: preview
  stack: preview =9.1, ga 9.2+
description: Monitor Streams data quality by tracking degraded documents, failed documents, quality scores, and ingestion trends over time.
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Manage your data quality with Streams [streams-data-quality]

When documents fail during ingestion, you can lose data without knowing what went wrong. Streams preserves failed documents and gives you the tools to find, understand, and fix data quality issues without leaving the Streams UI.

The Streams **Data quality** tab provides a single place to monitor and resolve data quality issues:

- **Failed documents are preserved, not dropped**: When a processing error occurs, data lands in a [failure store](#streams-data-quality-failure) instead of being lost, so nothing is silently discarded.
- **No separate infrastructure needed**.
- **See exactly what is failing and why**: The **Data quality** tab shows failure counts, error types, and sample messages, so you can identify problems immediately rather than searching for them.
- **Fix issues against the actual failing documents**: Instead of re-ingesting data from the source, you iterate on the processor using the exact documents that failed, with real-time validation before deploying the fix.

## Find and fix data quality issues [streams-data-quality-workflow]

Use the following steps to use Streams to identify failing documents, trace the source of failure, and deploy a fix.

:::::::{stepper}

::::::{step} Check the quality score

From the main **Streams** page, the **Data quality** column shows the health of each stream at a glance: **Good**, **Degraded**, or **Poor**. Filter by quality status to see streams that need attention, then click the quality score for a stream to open its **Data quality** tab.

:::{dropdown} How is the quality score calculated?

Streams uses the following {{esql}} queries to calculate the quality score for a stream:

- All documents (including failed documents): `FROM <stream-name>, <stream-name>::failures | STATS doc_count = COUNT(*)`
- Failed documents only: `FROM <stream-name>::failures | STATS failed_doc_count = COUNT(*)`
- Degraded documents: `FROM <stream-name> METADATA _ignored | WHERE _ignored IS NOT NULL | STATS degraded_doc_count = COUNT(*)`

Streams calculates data quality as follows:

- **Good:** Both the **Degraded documents** percentage and the **Failed documents** percentage are 0.
- **Degraded:** Either the **Degraded documents** percentage or the **Failed documents** percentage are greater than 0 and less than or equal to 3.
- **Poor:** Either the **Degraded documents** percentage or the **Failed documents** percentage are greater than 3.
:::

::::::

::::::{step} Review failures and trends

The **Data quality** tab shows a breakdown of what's wrong and when it started:

- **Failed documents**: Documents rejected during ingestion because of mapping conflicts or pipeline failures. Failed documents land in the [failure store](#streams-data-quality-failure) rather than being dropped.
- **Degraded documents**: Documents that were ingested but with fields silently ignored because of mapping issues or values that exceeded configured limits.
- **Quality score**: An overall health rating based on the percentage of failed and degraded documents.
- **Trends over time**: A time-series chart showing when the problem started and whether it's getting worse.

Use the chart to understand the scope of the issue before drilling into individual documents.
::::::

::::::{step} Enable the failure store

To inspect failed documents, you need to turn on the failure store. If the failure store is off, the **Failed documents** component shows **Enable failure store**, select it and set a retention period.

Once on, Streams captures all rejected documents in a `::failures` index. Each failed document includes the error message from the processor that caused the rejection, so you can trace the failure back to its source.

Refer to [Failure store](#streams-data-quality-failure) for permission requirements and setup details.
::::::

::::::{step} Fix and validate

Navigate to the **Processing** tab to edit the failing processor. The **Data preview** pane lets you test your changes against the actual documents that failed—so you can confirm the fix works against real data before deploying it.

When the preview looks right, select **Save changes**. Streams applies the updated pipeline to all future incoming documents.

Refer to [Process your documents](./parse-and-process.md) for detailed guidance on editing processors and using the data preview.
::::::

:::::::

## Failure store [streams-data-quality-failure]

A [failure store](../../../manage-data/data-store/data-streams/failure-store.md) is a secondary set of indices inside a data stream, dedicated to storing failed documents. Instead of losing documents that are rejected during ingestion, a failure store retains them in a `::failures` index, so you can review failed documents to understand what went wrong and how to fix it.

For example, for a stream called `my-stream`, Streams fetches all documents from the `my-stream::failures` index from within the specified time range in the date picker.

### Required permissions
:::{include} ../../_snippets/failure-store-permissions.md
:::

## Create a data quality alert [streams-data-quality-alert]

To get notified when the percentage of degraded documents in a stream exceeds a threshold, create an alert rule from the **Data quality** tab.

1. Open the **Data quality** tab for the stream you want to monitor.
2. Select **Create rule** ({icon}`bell`).
3. [Define the conditions](../incident-management/create-a-degraded-docs-rule.md#degraded-docs-rule-conditions) for your rule.