---
navigation_title: "Manage KIs"
description: Find and inspect Knowledge Indicators, edit, delete, or restore them in Kibana, and manage them through Context Engine workflow steps.
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

Inspect [Knowledge Indicators (KIs)](concepts.md#knowledge-indicators) in an [AI index](concepts.md#ai-indices) from {{kib}}, and change them through [workflows](/explore-analyze/workflows.md). To correct generated context, update and rerun the owning [automation](create-and-manage-automations.md). When a workflow needs to create, update, or delete individual KIs, use the dedicated {{context-engine}} workflow steps.

{applies_to}`stack: experimental 9.7+` You can also [edit, delete, and restore individual KIs](#change-ki-in-kibana) from their detail view in {{kib}}.

## Before you begin

Requirements depend on what you want to do:

- To inspect KIs:
    - An AI index that contains at least one KI.
    - The **Read** privilege for the **Context Engine** feature.
    - The `read` and `view_index_metadata` index privileges on the backing index (`ai-index-*`).
- {applies_to}`stack: experimental 9.7+` To edit, delete, or restore KIs in {{kib}}:
    - The **All** privilege for the **Context Engine** feature.
    - {{es}} write access to the backing index.
- To create, update, or delete KIs with workflows:
    - A custom AI index.
    - The **All** privilege for the **Context Engine** feature.
    - Permission to edit and run workflows.
    - {{es}} write access to the backing index. If an operation creates the backing index, you also need permission to create it.

You can inspect KIs in a [managed AI index](concepts.md#managed-ai-indices), but you cannot manage them directly. The Elastic feature that provides the AI index controls their lifecycle.

## Inspect a Knowledge Indicator in {{kib}}

The KI detail view shows the generated content and the metadata that identifies where it came from and when it changed.

1. Find **Context** in the navigation menu or use the global search field.
2. Open the AI index that contains the KI.
3. Select the **Knowledge Indicators** tab.
4. Optional: Filter the table by KI type.
5. Select a KI.
6. On the **Content** tab, review its generated content and metadata.
7. Select the **Document** tab to inspect the complete stored document.

Confirm that the title, type, status, and timestamps identify the KI you expected. The KI workflow steps automatically record provenance, including the workflow ID and run ID. Inspect these fields on the **Document** tab when you need to trace a KI to the workflow run that wrote it; you do not need to populate them yourself.

To assess whether the content is accurate and useful to an agent, refer to [Evaluate and improve Knowledge Indicators](evaluate-and-improve-knowledge-indicators.md).

{applies_to}`stack: experimental =9.6` The detail view is read-only.

<!-- Verify labels and add a screenshot after elastic/kibana#297691 and the planned follow-up KI visualization changes land.

The following image shows the Knowledge Indicators table and its type filter:

:::{image} images/knowledge-indicators-table.png
:alt: Knowledge Indicators table showing KI titles, types, statuses, and update times
:width: 800px
:screenshot:
:::
-->

## Edit, delete, or restore a Knowledge Indicator in {{kib}} [change-ki-in-kibana]

```{applies_to}
stack: experimental 9.7+
serverless: experimental
```

With the **All** privilege for the **Context Engine** feature, you can change an individual KI from its detail view. Users with the **Read** privilege do not see the edit, delete, or restore actions.

These actions change only the stored KI. They do not change the automation that generated it. If a later automation run would write the same KI again, update that automation as well.

### Edit a KI's content

1. Open the KI and select its **Content** tab.
2. Select **Edit**.
3. Change the KI's Markdown content in the editor.
4. Select **Save**.

You can edit only the content. The title, type, and other fields stay unchanged.

To discard your changes, select **Cancel**. If you leave the page while editing, {{kib}} asks you to confirm that you want to discard unsaved changes.

### Delete a KI [delete-ki-in-kibana]

1. Open the KI. If you are editing its content, save or cancel your changes first.
2. Select **Delete**. On the **Content** tab, **Delete** is in the overflow menu next to **Edit**.
3. Confirm the deletion.

Deleting a KI changes its lifecycle status to deleted and keeps the stored document. Retrieval excludes the KI, and the **Knowledge Indicators** tab hides it unless you filter by the **Deleted** status. You cannot edit a deleted KI until you restore it.

For a data-stream-backed AI index, each edit, delete, or restore appends a revision instead of changing the existing document. Discover can therefore show earlier revisions of the KI.

### Restore a deleted KI

1. On the AI index's **Knowledge Indicators** tab, set the **Status** filter to **Deleted**.
2. Select the KI.
3. Select **Restore**, then confirm.

Restoring a KI changes its lifecycle status back to active without changing its content. Agents can retrieve it again.

## Inspect raw Knowledge Indicator documents

Use [Discover](/explore-analyze/discover.md) when you need to compare several raw KI documents or inspect their stored fields.

1. On the AI index's **Knowledge Indicators** tab, select **View raw docs in Discover**.
2. In Discover, filter the documents to the KI or set of KIs you want to inspect.
3. Review their content, timestamps, lifecycle status, references, and provenance.

Use Discover for inspection. To retrieve KIs programmatically, use the list, describe, and query APIs described in [Query with APIs](retrieve-context-from-ai-index.md#query-with-apis). Manage KIs through their owning automation or the supported workflow steps instead of editing the backing index directly.

## Choose how to change a Knowledge Indicator

How you change a KI depends on how it was created and whether the change must survive future automation runs:

| Situation | Recommended action |
|---|---|
| Generated content is incomplete or incorrect | Edit the source or owning automation, then run the automation again. |
| One KI needs a correction that no automation run will replace | {applies_to}`stack: experimental 9.7+` [Edit its content in {{kib}}](#change-ki-in-kibana). |
| A deleted KI must be retrieved again | {applies_to}`stack: experimental 9.7+` [Restore it in {{kib}}](#change-ki-in-kibana). |
| A workflow maintains a long-lived KI across runs | Use `context-engine.updateKi` with a stable KI ID. |
| A workflow must write a new KI | Use `context-engine.createKi`. |
| A KI must no longer be retrieved | Use `context-engine.deleteKi`, then update its automation if another run would recreate it. |
| The KI belongs to a managed AI index | Do not change it directly. The Elastic feature that provides the AI index manages its KIs. |

Changing the automation is the preferred way to correct generated content because later runs reproduce the improvement. A direct update is appropriate when updating the KI is part of the workflow's intended design.

## Manage Knowledge Indicators in a workflow

Add KI management steps to an existing automation or to another workflow that intentionally maintains KIs:

1. Open the workflow in the [Workflows YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md).
2. Add the appropriate create, update, or delete step.
3. Test the workflow and inspect the step output.
4. Save and run the workflow.
5. Return to the AI index's **Knowledge Indicators** tab and confirm the result.

The following examples show the inputs for each operation.

### Create a KI

Use `context-engine.createKi` with `verifiers` to check a KI before writing it. This is the recommended approach when a KI must pass verification before it becomes available for retrieval. Set `ki_id` to a stable value when later runs must address the same logical KI.

The following example combines the built-in `esql-valid-syntax` verifier with a custom verifier workflow. `check-ki-content` is the name of the workflow defined in [Add a custom verifier](#add-custom-ki-verifier). Create and enable that workflow before running this step.

```yaml
- name: create_ki
  type: context-engine.createKi
  with:
    ai_index_id: "support-context"
    ki_id: "account-123-support-connection-456-cases"
    verifiers:
      - "esql-valid-syntax"
      - workflow_id: "check-ki-content"
    ki:
      type: "support.recurring_issue"
      title: "Recurring support case patterns"
      description: "Patterns found across the support cases analyzed by the workflow."
      content: "The cases in this support connection describe configuration and capacity issues. Use this context when investigating recurring support problems for this account."
      attributes:
        account_id: "account-123"
        connection_id: "support-connection-456"
        object_id: "cases"
      tags:
        - "support"
        - "recurring-issue"
```

Use `attributes` for structured identifiers that you need to filter on, such as the account, connection, and object represented by a KI. Use `content` to explain what the source contains and when it is useful. These attribute names are examples for this use case, not required KI fields. Storing an account or user identifier does not itself restrict access to the KI.

When one workflow writes KIs for multiple accounts or connections, give each logical KI a distinct, stable `ki_id`. The example combines the account, connection, and object identifiers so that later runs address the same KI without replacing another account's context.

For an index-backed AI index, another create operation with the same `ki_id` replaces the document. For a data-stream-backed AI index, it appends a revision.

When verification passes, the step writes the KI and returns its `id` and the `verification` results. If any verifier fails, the step returns `verification.passed: false` without an `id` and does not write the KI. Inspect `verification.results` for the outcome of each verifier. A completed step does not by itself mean that a KI was written.

For KIs that contain ES|QL, you can also add the built-in `esql-valid-syntax` and `esql-valid-runtime` verifiers. Parsing and running a query does not establish that it answers the intended question.

### Add a custom verifier [add-custom-ki-verifier]

A custom verifier is a workflow that receives the candidate KI as `inputs.ki` and returns a boolean `passed` result, with an optional `reason`. Create and enable the workflow in the same {{kib}} space as the calling workflow. In the `verifiers` list, set `workflow_id` to the verifier workflow's ID. {{kib}} derives the ID from the workflow's `name` when you create it, so the ID for this example is `check-ki-content`.

For example, this verifier rejects a KI when its `content` field is missing or empty:

```yaml
name: check-ki-content
enabled: true
triggers:
  - type: manual
inputs:
  - name: ki
    type: object
    required: true
outputs:
  - name: passed
    type: boolean
  - name: reason
    type: string
steps:
  - name: check_content
    type: if
    condition: 'inputs.ki.content: * and not inputs.ki.content: ""'
    steps:
      - name: accept_ki
        type: workflow.output
        with:
          passed: true
          reason: "The KI has content."
    else:
      - name: reject_ki
        type: workflow.output
        with:
          passed: false
          reason: "The KI content is missing or empty."
```

Test the verifier with a KI that contains content and one that does not. Confirm that it returns `passed: true` and `passed: false`, respectively. This example checks only whether content is present. Add checks appropriate to your use case to assess the generated information.

For the workflow input and output contract, refer to [](/explore-analyze/workflows/authoring-techniques/compose-workflows.md#workflows-compose-contract).

### Run verification separately

Use `context-engine.verifyKi` when your workflow needs to decide what to do with verification results independently of writing a KI. For example:

- Verify a candidate before creation, inspect the results, and intentionally write it even if a check fails. In this case, call `context-engine.createKi` without `verifiers` after applying your workflow's decision logic.
- Retrieve existing KIs in a separate workflow, verify them, and use `context-engine.deleteKi` to remove those that fail the required checks.

The step accepts the KI document and the same `verifiers` list as `context-engine.createKi`. It returns `passed` and `results` without writing, updating, or deleting the KI. Your workflow must explicitly perform any subsequent action.

### Update a KI

Use `context-engine.updateKi` to change selected fields of an existing KI. Fields that you omit remain unchanged, while arrays that you provide replace the existing arrays.

```yaml
- name: update_ki
  type: context-engine.updateKi
  with:
    ai_index_id: "support-context"
    ki_id: "account-123-support-connection-456-cases"
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
    ki_id: "account-123-support-connection-456-cases"
```

The step marks the KI as deleted and keeps the stored document. For a data-stream-backed AI index, it appends a revision with the deleted status and preserves the earlier revisions. A deleted KI remains visible in {{kib}} with the **Deleted** status.

{applies_to}`stack: experimental =9.6` For an index-backed AI index, the step removes the document instead.

{applies_to}`stack: experimental 9.7+` To restore a deleted KI, refer to [Restore a deleted KI](#restore-a-deleted-ki).

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
5. If the KI includes identifying attributes, confirm that they match the intended account, connection, and source object.

If the workflow completed but the expected KI was not written, inspect any configured verifier results. Verification failure prevents `context-engine.createKi` from writing the KI.
