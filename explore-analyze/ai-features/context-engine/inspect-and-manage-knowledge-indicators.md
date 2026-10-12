---
navigation_title: "Manage KIs"
description: Find and inspect Knowledge Indicators, then create, update, or delete them through supported Context Engine workflow steps.
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

# Inspect and manage Knowledge Indicators in {{context-engine}}

:::{include} _snippets/hidden-docs-notice.md
:::

[Knowledge Indicators (KIs)](concepts.md#knowledge-indicators) in an [AI index](concepts.md#ai-indices) can be inspected in {{kib}}, while repeatable changes are made through [workflows](/explore-analyze/workflows.md). Update and rerun the owning [automation](create-and-manage-automations.md) to correct generated context, or use dedicated {{context-engine}} workflow steps when a workflow needs to create, update, or delete individual KIs.

## Before you begin

Requirements depend on what you want to do:

- To inspect KIs:
    - An AI index that contains at least one KI.
    - The **Read** privilege for the **Context Engine** feature.
    - The `read` and `view_index_metadata` index privileges on the backing index (`ai-index-*`).
- To create, update, or delete KIs:
    - A custom AI index.
    - The **All** privilege for the **Context Engine** feature.
    - Permission to edit and run workflows.
    - {{es}} write access to the backing index. If an operation creates the backing index, you also need permission to create it.

You can inspect KIs in a [managed AI index](concepts.md#managed-ai-indices), but its owning Elastic integration controls their lifecycle.

## Inspect a KI in {{kib}}

The KI detail view shows the generated content and the metadata that identifies where it came from and when it changed.

1. Find **Context** in the navigation menu or use the global search field.
2. Open the AI index that contains the KI.
3. Select the **Knowledge Indicators** tab.
4. Optional: Filter the table by KI type.
5. Select a KI.
6. On the **Content** tab, review its generated content and metadata.
7. Select the **Document** tab to inspect the complete stored document.

Confirm that the title, type, status, timestamps, and provenance identify the KI and the workflow run you expected.

The detail view is read-only. To assess whether the content is accurate and useful to an agent, refer to [Evaluate and improve Knowledge Indicators](evaluate-and-improve-knowledge-indicators.md).

<!-- Verify labels and add a screenshot after elastic/kibana#295749 merges.

The following image shows the Knowledge Indicators table and its type filter:

:::{image} images/knowledge-indicators-table.png
:alt: Knowledge Indicators table showing KI titles, types, statuses, and update times
:width: 800px
:screenshot:
:::
-->

## Inspect raw KI documents

Use [Discover](/explore-analyze/discover.md) when you need to compare several raw KI documents or inspect their stored fields.

1. On the AI index's **Knowledge Indicators** tab, select **View raw docs in Discover**.
2. In Discover, filter the documents to the KI or set of KIs you want to inspect.
3. Review their content, timestamps, lifecycle status, references, and provenance.

Use Discover for inspection. Manage KIs through their owning automation or the supported workflow steps instead of editing the backing index directly.

## Choose how to change a KI

How you change a KI depends on how it was created and whether the change must survive future automation runs:

| Situation | Recommended action |
|---|---|
| Generated content is incomplete or incorrect | Edit the source or owning automation, then run the automation again. |
| A workflow maintains a long-lived KI across runs | Use `context-engine.updateKi` with a stable KI ID. |
| A workflow must write a new KI | Use `context-engine.createKi`. |
| A KI must no longer be retrieved | Use `context-engine.deleteKi`, then update its automation if another run would recreate it. |
| The KI belongs to a managed AI index | Do not change it directly. The owning Elastic integration manages it. |

Changing the automation is the preferred way to correct generated content because later runs reproduce the improvement. A direct update is appropriate when updating the KI is part of the workflow's intended design.

## Manage KIs in a workflow

Add KI management steps to an existing automation or to another workflow that intentionally maintains KIs:

1. Open the workflow in the [Workflows YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md).
2. Add the appropriate create, update, or delete step.
3. Test the workflow and inspect the step output.
4. Save and run the workflow.
5. Return to the AI index's **Knowledge Indicators** tab and confirm the result.

The following examples show the inputs for each operation.

### Create a KI

Use `context-engine.createKi` to write a KI. Set `ki_id` to a stable value when later runs must address the same logical KI.

```yaml
- name: create_ki
  type: context-engine.createKi
  with:
    ai_index_id: "support-context"
    ki_id: "support-case-patterns"
    ki:
      type: "support.recurring_issue"
      title: "Recurring support case patterns"
      description: "Patterns found across the support cases analyzed by the workflow."
      content: "The reviewed cases show recurring configuration and capacity issues."
      tags:
        - "support"
        - "recurring-issue"
```

For an index-backed AI index, another create operation with the same `ki_id` replaces the document. For a data-stream-backed AI index, it appends a revision.

The step returns the created document's `id`. If you configure verifiers and any verifier fails, the step does not write the KI and the output has no `id`.

### Update a KI

Use `context-engine.updateKi` to change selected fields of an existing KI. Fields that you omit remain unchanged, while arrays that you provide replace the existing arrays.

```yaml
- name: update_ki
  type: context-engine.updateKi
  with:
    ai_index_id: "support-context"
    ki_id: "support-case-patterns"
    ki:
      description: "Reviewed patterns found across recent support cases."
      tags:
        - "support"
        - "recurring-issue"
        - "reviewed"
```

The step returns `updated` when it changes the KI and `noop` when the supplied values already match the stored document. It fails if the AI index or KI does not exist.

For an index-backed AI index, the step updates the stored document. For a data-stream-backed AI index, it appends a revision with the supplied changes.

### Delete a KI

Use `context-engine.deleteKi` to prevent a KI from appearing in normal retrieval results.

```yaml
- name: delete_ki
  type: context-engine.deleteKi
  with:
    ai_index_id: "support-context"
    ki_id: "support-case-patterns"
```

For an index-backed AI index, the step removes the document. For a data-stream-backed AI index, it marks the KI as deleted and preserves its revisions. A deleted KI can therefore remain visible in the inspection UI with the **Deleted** status.

Deleting a KI does not change the workflow that generated it. If a later run would recreate the KI, update or stop that automation as well.

:::{tip}
KI write operations do not wait for an {{es}} refresh by default. Set `refresh: true` when a later step in the same workflow run must immediately read, update, or delete the KI.
:::

## Verify the result

After the workflow runs, confirm the intended outcome:

1. Inspect the management step in the workflow execution and confirm that it completed successfully.
2. Open the AI index's **Knowledge Indicators** tab.
3. Find the KI by its title and type, then open its details.
4. Confirm that its ID, content, update time, status, and provenance match the workflow run.

If the workflow completed but the expected KI was not written, inspect any configured verifier results. Verification failure prevents `context-engine.createKi` from writing the KI.
