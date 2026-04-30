---
navigation_title: "Dashboards and visualizations"
description: "Create, edit, and save Kibana dashboards and visualizations through natural language chat with Agent Builder agents."
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Dashboards and visualizations in {{agent-builder}} chat

Agents can create and manage [dashboards](/explore-analyze/dashboards.md) and [visualizations](/explore-analyze/visualize.md) directly in the conversation. Send a message like "create a dashboard to monitor host CPU and memory usage" and the agent builds a dashboard with {{esql}}-powered visualization panels.

This functionality is powered by the built-in [`dashboard-management`](builtin-skills-reference.md#agent-builder-dashboard-management-skill) and [`visualization-creation`](builtin-skills-reference.md#agent-builder-visualization-creation-skill) skills, along with the [dashboard tools](tools/builtin-tools-reference.md#dashboard-tools) and [visualization platform tools](tools/builtin-tools-reference.md#platform-core-tools).

## When to use agent-generated dashboards

Building dashboards manually requires knowing which indices to query, how to write the right visualizations, and how to arrange panels. Agent-generated dashboards let you skip that process and go from a question to a working dashboard in seconds. This is particularly useful when you need to:

- **Get started with dashboards**: If you are new to {{kib}} dashboards, you can learn by asking the agent to create visualizations and exploring the results. This lowers the barrier to entry and helps you understand dashboard capabilities without needing to learn the editor first.
- **Investigate ad hoc**: During an incident, ask the agent to build a dashboard showing the relevant metrics so you can triage without leaving the conversation.
- **Explore unfamiliar data**: When you are working with a new data source, ask the agent to visualize key fields so you can understand what is available before building something more permanent.
- **Prototype and iterate**: Describe the dashboard you want in plain language, refine it through conversation, and save it only when you are satisfied with the result.

:::{tip}
The full-screen [standalone chat mode](standalone-and-flyout-modes.md#standalone-mode) provides the best experience for working with dashboards. Dashboards also work in [sidebar mode](standalone-and-flyout-modes.md#sidebar-mode), but the larger canvas area in standalone mode makes it easier to preview and interact with dashboard content.
:::

## How dashboards appear in chat

When an agent creates a dashboard, it describes the contents in the conversation and attaches the dashboard to the message. Dashboards are both inputs and outputs: the agent can reason about the panels in an attached dashboard when answering follow-up questions.

The following example walks through creating a dashboard from a natural language request.

:::::{stepper}
::::{step} Ask the agent to create a dashboard

Describe what you want to visualize. The agent creates the dashboard and responds with a description of the contents and a **Preview** button.

:::{image} images/agent-builder-dashboard-chat-response.png
:screenshot:
:alt: Agent chat response showing a created Web Traffic Analysis Dashboard with a Preview button and a breakdown of the included sections and metrics
:::
::::
::::{step} Preview the dashboard

Select **Preview** to open the dashboard in a canvas alongside the conversation.

:::{image} images/agent-builder-dashboard-canvas-preview.png
:screenshot:
:alt: Full-screen chat with the conversation on the left and a dashboard canvas preview on the right showing metrics, charts, and trend panels
:::
::::
::::{step} Save or refine

From here, you can use the buttons in the canvas toolbar:

:::{image} images/agent-builder-dashboard-save-or-edit-buttons.png
:screenshot:
:alt: Edit in Dashboards and Save buttons in the dashboard canvas toolbar
:width: 250px
:::

Select **Save** to [save the dashboard](#save-a-dashboard) as a {{kib}} saved object. Select **Edit in Dashboards** to open the dashboard in the [Dashboards app](/explore-analyze/dashboards.md) for further editing.

You can also continue chatting to refine the dashboard. For example, ask the agent to add panels, change chart types, update metrics, or rearrange the layout.

Individual visualizations display inline in the conversation when you ask for a single chart or metric.
::::
:::::

## Manage dashboards

Agent-created dashboards start as in-memory attachments in the conversation. You can save them as {{kib}} objects when you are ready, and pull in changes if the saved dashboard is edited outside the conversation.

### In-memory dashboards

Dashboards that agents create are **in-memory** by default. They exist only as conversation attachments and are not saved as {{kib}} objects until you choose to save them. This means you can iterate on a dashboard through conversation without creating unnecessary saved objects.

### Save a dashboard

To save an agent-created dashboard as a {{kib}} saved object:

1. Select **Save** on the dashboard preview.
2. Review the title and description (pre-filled by the agent), add optional tags, and configure permissions.
3. Select **Save**.

:::{image} images/agent-builder-dashboard-save-dialog.png
:screenshot:
:alt: Save as new dashboard dialog with title, description, tags, and permissions fields
:width: 450px
:::

After saving, you can open the dashboard in the [Dashboards app](/explore-analyze/dashboards.md) for further editing using the full dashboard editor.

:::{important}
Saving a new version of the dashboard from the same conversation overwrites the existing saved dashboard.
:::

### Sync in-memory and saved dashboards

If you save a dashboard and then edit it in the Dashboards app, the conversation detects the changes. A notification appears with the message **"Some attachments are outdated"**, and you can select **Use updated versions** to pull the latest changes back into the conversation.

:::{image} images/agent-builder-dashboard-outdated-notification.png
:screenshot:
:alt: Notification showing that a dashboard attachment is outdated with options to use the updated version or dismiss
:width: 550px
:::

The agent preserves your external edits when making further updates.
You can also go back to any previously generated version of a dashboard in the conversation and save that version instead.

## Supported panel types

Agents create [{{esql}}](/explore-analyze/visualize/esorql.md)-powered visualizations. If a dashboard contains [data view](/explore-analyze/find-and-organize/data-views.md)-based visualizations, the agent asks to replace them with {{esql}} equivalents when making changes.

Agents can also create markdown panels and collapsible sections.

## Related pages

- [Dashboards](/explore-analyze/dashboards.md)
- [Chat with {{agent-builder}} agents](chat.md)
% TODO: Add once docs-content#5927 merges:
% - [Create dashboards programmatically](/explore-analyze/dashboards/create-dashboards-programmatically.md)
