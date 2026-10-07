---
navigation_title: Enhance using AI
description: Use Agent Builder to improve an existing Kibana dashboard. Choose appearance-only or content changes, review the result, and save or discard it.
applies_to:
  stack: experimental 9.6+
  serverless: experimental
products:
  - id: kibana
type: how-to
---

# Enhance a dashboard with AI [enhance-dashboard-with-ai]

When a dashboard you built needs tidying, an {{agent-builder}} agent can improve it for you instead of you rebuilding it by hand. The agent determines what your panels measure, then rewrites the dashboard text, rearranges the panels, and applies the default chart styling. You review the result in the dashboard, then save it or discard it.

## Before you begin [enhance-dashboard-requirements]

- You need the **All** privilege for the **Dashboard** feature.
- You need [access to {{agent-builder}}](/explore-analyze/ai-features/agent-builder/permissions.md), with a [model](/explore-analyze/ai-features/agent-builder/models.md) configured.
- The dashboard must have at least one panel that runs an {{esql}} query. Otherwise, **Enhance** doesn't appear.
- If you have unsaved edits that you want to keep, save the dashboard first. Discarding the agent's changes returns the dashboard to its last saved version.

## Enhance the dashboard [enhance-dashboard-steps]

1. Open the dashboard in **Edit** mode.
2. Select **Enhance** in the dashboard header.

   :::{image} /explore-analyze/images/dashboard-enhance-button.png
   :alt: Dashboard in edit mode with the Enhance button in the header and its tooltip, Improve the content and style of your dashboard using AI. The dashboard has a humidity metric, a pie chart, and a tag cloud, with empty space to the right.
   :screenshot:
   :::

   A new conversation opens in the [chat beside the dashboard](/explore-analyze/ai-features/agent-builder/standalone-and-flyout-modes.md#sidebar-mode), with the dashboard attached. The agent starts reviewing the dashboard right away.
3. When the agent asks how to enhance the dashboard, choose an option. Each option lists the main changes the agent plans for your dashboard, so you can review them first.

   - **Appearance and content** improves how the dashboard looks and reads, and can also add, change, replace, or remove panels.
   - **Appearance only** keeps your panels and their queries, and improves how the dashboard looks and reads.

   To add your own instructions, such as panels to keep, type them in the **Be more specific** field.

   :::{image} /explore-analyze/images/dashboard-enhance-mode-question.png
   :alt: The agent's question, How would you like to enhance this dashboard, with the Appearance and content, Appearance only, and Be more specific options, and the Skip question and Submit buttons.
   :screenshot:
   :width: 450px
   :::

   Then select **Submit**. If you skip the question, or your instructions don't say which option you want, the agent applies **Appearance and content**. For details, refer to [What each option changes](#enhance-dashboard-modes).
4. Wait for the agent to finish. The agent summarizes its changes in the conversation, and the changes appear in the dashboard you have open.

   :::{image} /explore-analyze/images/dashboard-enhance-result.png
   :alt: The enhanced dashboard, retitled and organized into Key metrics and Trends over time sections, with a City control. The chat beside it lists what the agent changed and added.
   :screenshot:
   :::
5. Review the changes in the dashboard.
6. Save the dashboard to keep the changes. If you don't want them, [discard the changes](#enhance-dashboard-discard) instead.

## How the agent enhances a dashboard [enhance-dashboard-how-it-works]

**Enhance** starts the [`dashboards` skill](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-dashboard-management-skill) in a new conversation, with your dashboard attached. The agent first reads the dashboard and the field mappings of the indices its panels query. From these, it works out what the dashboard measures and what it's missing, and proposes changes for each option. After you choose, it applies the changes to the dashboard you have open, checks them against its plan, and reports what it did.

The agent decides the changes for each dashboard, so two runs on the same dashboard can give different results. When the first run is done, you can keep improving the dashboard in the same conversation.

## What each option changes [enhance-dashboard-modes]

The two options differ in how much of the dashboard the agent can change:

| | **Appearance only** | **Appearance and content** |
|---|---|---|
| Panels, queries, controls, and time range | No panels added, replaced, or removed. Queries, controls, and the time range don't change | The agent can add, change, or replace panels, change panel queries, and add controls. It removes panels that duplicate another panel or don't fit the dashboard's purpose |
| Dashboard title, description, and text panels | Rewritten to match what the panels measure | Rewritten to match what the panels measure |
| Layout | Panels rearranged and grouped into sections where that makes the dashboard clearer | Panels rearranged and grouped into sections where that makes the dashboard clearer |
| {{esql}} visualizations | Chart styling reset to the defaults, which replaces any custom styling | Chart styling reset to the defaults, which replaces any custom styling |
| Other panels, except text panels | Moved or resized only | Replaced with an {{esql}} visualization when the agent can re-create the panel in {{esql}}. Otherwise, moved or resized only |

For the layout practices the agent applies, refer to [Dashboard grid layout and best practices](arrange-panels.md#dashboard-grid-layout).

## Discard the changes [enhance-dashboard-discard]

If you don't want to keep the agent's changes, open the **Save** menu and select **Reset changes** before you save. Resetting returns the dashboard to its last saved version, so it also discards any unsaved edits you made yourself. After you save, you can no longer discard the changes in one step. For details, refer to [Reset dashboard changes](open-dashboard.md#reset-the-dashboard).

## Next steps [enhance-dashboard-next-steps]

- Ask the agent for more changes in the same conversation, for example to change a chart type or add a panel. The changes appear in the dashboard you have open.
- To enhance the dashboard again without the **Enhance** button, open a new conversation while you edit the dashboard. Then [type `/dashboards`](/explore-analyze/ai-features/agent-builder/skills.md) followed by your request, for example `/dashboards Enhance this dashboard, appearance only`. When your request says what to change, the agent doesn't ask which option to apply.
- Fine-tune the layout yourself. Refer to [Organize dashboard panels](arrange-panels.md).

## Related pages [enhance-dashboard-related-pages]

- [Dashboards and visualizations in {{agent-builder}} chat](/explore-analyze/ai-features/agent-builder/agent-builder-dashboards-and-visualizations.md)
- [Create dashboards using AI](create-dashboards-using-ai.md)
- [`dashboards` skill](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-dashboard-management-skill)
