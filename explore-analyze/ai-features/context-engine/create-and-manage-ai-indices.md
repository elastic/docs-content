---
navigation_title: "Manage AI indices"
description: Create, inspect, update, and delete a custom AI index and its associated resources.
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

# Create and manage AI indices

:::{include} _snippets/hidden-docs-notice.md
:::

An AI index groups the sources, automations, and Knowledge Indicators (KIs) that agents retrieve as context for a defined subject. Its name and description help agents decide when that context is relevant. Create and maintain AI indices interactively in {{kib}} or programmatically with the {{context-engine}} APIs. You can update or delete AI indices that you create. [Managed AI indices](concepts.md#managed-ai-indices) are read-only.

## Before you begin

Turn on the `contextEngine:enabled` advanced setting in the current {{kib}} space. You also need the **All** privilege for the **Context Engine** feature. To remove associated workflow automations when deleting an AI index, you also need permission to delete workflows. To delete its backing index and KIs, you need the `delete_index` index privilege on that index.

Define the purpose and boundaries of the AI index before creating it. For planning guidance, refer to [Define the AI index's purpose](build-and-maintain-ai-index.md#define-the-ai-indexs-purpose).

## Create an AI index

Create an AI index in {{kib}} for an interactive setup, or use the API for programmatic provisioning.

### Use the UI

Create a custom AI index as follows:

1. Open **Context** from the {{kib}} navigation.
2. Select **Create AI Index**.
3. Enter a **Name**. It must start with a lowercase letter or number and can contain lowercase letters, numbers, hyphens, and underscores.
4. Enter a **Description** that states what the AI index is for and what its KIs contain. Include example questions the KIs should help answer and any known gaps in the information.
5. Optional: Under **Agent traces**, select the traces that you want to use as feedback about how agents use the context.
6. Select **Create AI index**.

<!--
:::{image} images/create-ai-index.png
:alt: Create AI index page showing the Name, Description, and Agent traces sections
:width: 700px
:screenshot:
:::
-->

The AI index opens with a confirmation message. Its **Sources** section is empty, and its **Automations** section remains locked until you add at least one source.

The name also determines the generated {{es}} index used to store KIs. You cannot rename an AI index in the UI after creating it.

### Use the API [create-ai-index-api]

Use the [create AI index API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-context-engine-ai-index) when you need to provision AI indices programmatically. The request defines the AI index ID, its {{es}} destination, and its initial description, sources, automations, and traces.

For example, run the following request in [Console](/explore-analyze/query-filter/tools/console.md):

```console
POST kbn:/api/context_engine/ai_index
{
  "id": "support_context",
  "description": "Context about support cases, including recurring issues, affected products, resolution patterns, and known gaps.",
  "dest": {
    "type": "index",
    "value": "ai-index-idx-support_context"
  },
  "sources": [],
  "automations": [],
  "traces": []
}
```

The response returns `"status": "created"`. Add sources and automations in later API requests, or include them in the create request when their definitions are already known. The API reference provides the complete request and response schemas.

## Inspect AI indices

View AI indices in {{kib}}, or retrieve their definitions with the API.

### Use the UI

In {{kib}}, open **Context** to view the AI indices available in the current space, then select one to inspect its configuration and generated KIs.

### Use the API

For programmatic access, use the following APIs:

- [List AI indices](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-context-engine-ai-index) returns the AI indices available to the caller.
- [Get an AI index](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-context-engine-ai-index-aiindexid) returns the complete definition of one AI index.

## Update an AI index

In {{kib}}, you can update the description that agents and generated automation workflows use. With the API, you can update the complete AI index definition.

### Use the UI

Keep the description aligned with the context the AI index actually contains. The description shapes generated automation workflows and helps agents decide whether the AI index is relevant.

Update it as follows:

1. Open **Context**, then select the AI index.
2. In **Description**, select **Edit**.
3. Update the description, then select **Save**.
4. Confirm that the updated description appears on the AI index page.

### Use the API [update-ai-index-api]

Use the [create or update AI index API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-put-context-engine-ai-index-aiindexid) to update an AI index programmatically. The request body replaces the complete AI index record. Include its destination and every source, automation, and trace that you want to preserve.

For example, the following request updates the description of the AI index created previously:

```console
PUT kbn:/api/context_engine/ai_index/support_context
{
  "description": "Context about support cases, including recurring issues, affected products, resolution patterns, known gaps, and verified queries for current case details.",
  "dest": {
    "type": "index",
    "value": "ai-index-idx-support_context"
  },
  "sources": [],
  "automations": [],
  "traces": []
}
```

## Delete an AI index [delete-an-ai-index]

Delete a custom AI index from {{kib}} or with the API. In either case, decide whether to preserve or delete its generated KIs and attached workflow automations.

### Use the UI

Deleting an AI index always removes its {{context-engine}} entry. You can also remove the generated KIs and workflow automations associated with it.

Delete an AI index as follows:

1. Open **Context**.
2. Open the actions menu for the AI index, then select **Delete AI index**.
3. In the confirmation dialog, select which associated resources to remove:

    - **Also delete the backing index `<index>` and its Knowledge Indicators**: selected by default. Clear it to keep the generated KIs and their {{es}} index.
    - **Also delete its _N_ automations**: selected by default when the AI index has automations and you have permission to delete workflows. Otherwise, it's unavailable.

4. Select **Delete AI index**.
5. Confirm that the AI index no longer appears in **Context**.

<!--
:::{image} images/delete-ai-index.png
:alt: Delete AI index confirmation dialog showing the options for deleting generated Knowledge Indicators and attached automations
:width: 600px
:screenshot:
:::
-->

If you preserve an associated resource, deleting the AI index does not delete that resource. Agents can no longer discover or retrieve from the deleted AI index through {{context-engine}}.

You cannot edit or delete a managed AI index. Its owning Elastic integration controls its configuration and lifecycle.

### Use the API [delete-ai-index-api]

Use the [delete AI index API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-delete-context-engine-ai-index-aiindexid) for scripted cleanup. By default, the API deletes only the {{context-engine}} entry and preserves its {{es}} destination, KIs, and attached workflows. Set the cleanup parameters explicitly when you also want to delete those resources.

For example, the following request deletes the entry, its destination and KIs, and its attached workflow automations:

```console
DELETE kbn:/api/context_engine/ai_index/support_context?delete_knowledge_indicators=true&delete_automations=true
```

Check the response's `errors` array for any resource that could not be deleted after the AI index entry was removed.
