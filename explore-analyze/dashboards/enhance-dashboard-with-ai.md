---
navigation_title: Enhance using AI
description: Let an Agent Builder agent improve a Kibana dashboard you already built. Decide how much it can change, review the result, then keep or discard it.
applies_to:
  stack: experimental 9.6+
  serverless: experimental
products:
  - id: kibana
type: how-to
---

# Enhance a dashboard with AI [enhance-dashboard-with-ai]

If a dashboard you built needs tidying, you can let an {{agent-builder}} agent improve it instead of rebuilding it by hand. The agent works out what your panels measure, then gives the dashboard clearer text, a tidier layout, and consistent chart styling. Nothing is kept until you review the result and save the dashboard.

## Before you begin [enhance-dashboard-requirements]

- You need the **All** privilege for the **Dashboard** feature.
- You need [access to {{agent-builder}}](/explore-analyze/ai-features/agent-builder/permissions.md), with a [model](/explore-analyze/ai-features/agent-builder/models.md) configured.
- The dashboard must have at least one panel that runs an {{esql}} query. Otherwise, **Enhance** doesn't appear.
- If you have unsaved edits that you want to keep, save the dashboard first. That way, you can discard the agent's changes later without losing your own work.

## Enhance the dashboard [enhance-dashboard-steps]

1. Open the dashboard in **Edit** mode.
2. Select **Enhance** in the dashboard header.

   :::{image} /explore-analyze/images/dashboard-enhance-button.png
   :alt: Dashboard in edit mode with the Enhance button in the header and its tooltip, Improve the content and style of your dashboard using AI. The dashboard has a humidity metric, a pie chart, and a tag cloud, with empty space to the right.
   :screenshot:
   :::

   The [chat opens beside the dashboard](/explore-analyze/ai-features/agent-builder/standalone-and-flyout-modes.md#sidebar-mode) in a new conversation, with your dashboard attached, and the agent starts reviewing it right away.
3. When the agent asks how you'd like to enhance the dashboard, select the option that fits. Each option lists the main changes the agent plans for your dashboard, so you know what to expect before you decide.

   - **Appearance and content** improves how the dashboard looks and reads, and can also add, change, replace, or remove panels.
   - **Appearance only** keeps your panels and their queries, and improves how the dashboard looks and reads.

   You can also give the agent your own instructions in the **Be more specific** field, for example to name panels it must keep.

   :::{image} /explore-analyze/images/dashboard-enhance-mode-question.png
   :alt: The agent's question, How would you like to enhance this dashboard, with the Appearance and content, Appearance only, and Be more specific options, and the Skip question and Submit buttons.
   :screenshot:
   :width: 450px
   :::

   When you're ready, select **Submit**. If you skip the question, or your instructions don't say which option you want, the agent applies **Appearance and content**. For details, refer to [What each option changes](#enhance-dashboard-modes).
4. Wait while the agent works. When it's done, it summarizes its changes in the conversation, and you can see the result in the dashboard you have open.

   :::{image} /explore-analyze/images/dashboard-enhance-result.png
   :alt: The enhanced dashboard, retitled and organized into Key metrics and Trends over time sections, with a City control. The chat beside it lists what the agent changed and added.
   :screenshot:
   :::
5. Review the changes in the dashboard.
6. To keep the changes, save the dashboard. If you'd rather not keep them, [discard them](#enhance-dashboard-discard) instead.

## How the agent enhances a dashboard [enhance-dashboard-how-it-works]

When you select **Enhance**, {{agent-builder}} runs the [`dashboards` skill](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-dashboard-management-skill) on your dashboard. The agent first reads the dashboard and the field mappings of the indices its panels query. From these, it works out what the dashboard measures and what it's missing, and proposes changes for each option. After you select an option, it applies the changes to the dashboard you have open, checks them against its plan, and reports what it did.

Because the agent tailors its changes to each dashboard, two runs on the same dashboard can give different results. Once the first run is done, you can keep refining the dashboard in the same conversation.

## What each option changes [enhance-dashboard-modes]

The two options differ in how much of the dashboard the agent can change:

| | **Appearance only** | **Appearance and content** |
|---|---|---|
| Panels, queries, controls, and time range | No panels added, replaced, or removed. Queries, controls, and the time range don't change | The agent can add, change, or replace panels, change panel queries, and add controls. It removes panels that duplicate another panel or don't fit the dashboard's purpose |
| Dashboard title, description, and text panels | Rewritten to match what the panels measure | Rewritten to match what the panels measure |
| Layout | Panels rearranged and grouped into sections where that makes the dashboard clearer | Panels rearranged and grouped into sections where that makes the dashboard clearer |
| {{esql}} visualizations | Chart styling reset to the defaults, which replaces any custom styling | Chart styling reset to the defaults, which replaces any custom styling |
| Other panels, except text panels | Moved or resized only | Replaced with an {{esql}} visualization when the agent can re-create the panel in {{esql}}. Otherwise, moved or resized only |

In both cases, the agent arranges panels using the practices described in [Dashboard grid layout and best practices](arrange-panels.md#dashboard-grid-layout). You can apply the same practices when you arrange panels yourself.

## Discard the changes [enhance-dashboard-discard]

If you'd rather not keep the agent's changes, open the **Save** menu and select **Reset changes** before you save. Resetting returns the dashboard to its last saved version, so it also discards any unsaved edits you made yourself. After you save, you can no longer discard the changes in one step. For details, refer to [Reset dashboard changes](open-dashboard.md#reset-the-dashboard).

## Next steps [enhance-dashboard-next-steps]

- Ask the agent for more changes in the same conversation, for example to change a chart type or add a panel. The changes appear in the dashboard you have open.
- To enhance the dashboard again later, you don't need the **Enhance** button. While you edit the dashboard, open a new conversation and enter [`/dashboards`](/explore-analyze/ai-features/agent-builder/skills.md) followed by your request, for example `/dashboards Enhance this dashboard, appearance only`. If your request already says what to change, the agent skips the question.
- To fine-tune the layout yourself, refer to [Organize dashboard panels](arrange-panels.md).

## Related pages [enhance-dashboard-related-pages]

- [Dashboards and visualizations in {{agent-builder}} chat](/explore-analyze/ai-features/agent-builder/agent-builder-dashboards-and-visualizations.md)
- [Create dashboards using AI](create-dashboards-using-ai.md)
- [`dashboards` skill](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-dashboard-management-skill)
