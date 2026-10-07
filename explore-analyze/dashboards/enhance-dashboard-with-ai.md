---
navigation_title: Enhance using AI
description: Improve a Kibana dashboard you already built with an Agent Builder agent. Decide how much the agent can change, review the result, then keep or discard it.
applies_to:
  stack: experimental 9.6+
  serverless: experimental
products:
  - id: kibana
type: how-to
---

# Enhance a {{kib}} dashboard with AI [enhance-dashboard-with-ai]

If a dashboard you built feels cluttered or hard to read, you can let an {{agent-builder}} agent improve it instead of reworking it by hand. The agent looks at what your panels actually measure, then gives the dashboard clearer text, a tidier layout, and consistent chart styling. You can also let it fill the gaps, for example by adding the trends or breakdowns that your data supports. The changes stay unsaved until you review them and decide to keep them.

## Before you begin [enhance-dashboard-requirements]

To enhance a dashboard, you need:

- The **All** privilege for the **Dashboard** feature.
- [Access to {{agent-builder}}](/explore-analyze/ai-features/agent-builder/permissions.md), with a [model](/explore-analyze/ai-features/agent-builder/models.md) configured.
- At least one panel on the dashboard that runs an {{esql}} query. The **Enhance** option appears only on dashboards that have one.

If you have unsaved edits that you want to keep, save the dashboard first. That way, you can discard the agent's changes later without losing your own work.

## Enhance the dashboard [enhance-dashboard-steps]

1. Open the dashboard in **Edit** mode.
2. In the application menu, select **Enhance**.

   :::{image} /explore-analyze/images/dashboard-enhance-button.png
   :alt: Dashboard in edit mode with the Enhance button in the application menu and its tooltip, Improve the content and style of your dashboard using AI. The dashboard has a humidity metric, a pie chart, and a tag cloud.
   :screenshot:
   :::

   The chat opens in the [sidebar](/explore-analyze/ai-features/agent-builder/standalone-and-flyout-modes.md#sidebar-mode) in a new conversation, with your dashboard attached, and the agent starts reviewing it right away.
3. When the agent asks how you'd like to enhance the dashboard, select the option that fits. Each option lists the main changes the agent plans for your dashboard, so you know what to expect before you decide.

   - **Appearance and content** improves how the dashboard looks and reads, and also lets the agent add, change, replace, or remove panels.
   - **Appearance only** keeps your panels and their queries as they are, and focuses on how the dashboard looks and reads.

   You can also give the agent your own instructions in the **Be more specific** field, for example to name panels it must keep.

   :::{image} /explore-analyze/images/dashboard-enhance-mode-question.png
   :alt: The agent's question, How would you like to enhance this dashboard, with the Appearance and content, Appearance only, and Be more specific options, and the Skip question and Submit buttons.
   :screenshot:
   :width: 450px
   :::

   When you're ready, select **Submit**. If you skip the question, or your instructions don't say which option you want, the agent applies **Appearance and content**. To compare the two options in detail, refer to [What each option changes](#enhance-dashboard-modes).
4. Wait while the agent works. When it's done, the agent summarizes its changes in the conversation, and you can see the result in the dashboard you have open.

   :::{image} /explore-analyze/images/dashboard-enhance-result.png
   :alt: The enhanced dashboard, retitled and organized into Key metrics and Trends over time sections, with a City control. The chat beside it lists what the agent changed and added.
   :screenshot:
   :::
5. Review the dashboard. If you want something different, ask the agent for adjustments in the same conversation, for example to change a chart type or add a panel.
6. To keep the changes, save the dashboard. If you'd rather not keep them, [discard them](#enhance-dashboard-discard) instead.

## How the agent enhances a dashboard [enhance-dashboard-how-it-works]

When you select **Enhance**, {{agent-builder}} runs the [`dashboards` skill](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-dashboard-management-skill) on your dashboard. The agent then:

1. Reads the dashboard and the field mappings of the indices behind its panels. This tells it what the dashboard measures, and what your data could show that the dashboard doesn't show yet.
2. Proposes two sets of changes, one limited to appearance and one with a more complete content review, and asks which one you want.
3. Applies the changes to the dashboard you have open.
4. Checks the result against its plan, and summarizes its changes in the conversation.

Because the agent tailors its changes to each dashboard, two runs on the same dashboard can give different results.

## What each option changes [enhance-dashboard-modes]

Both options rewrite the dashboard title, description, and Markdown panels to match what the panels measure.

- **Appearance only** keeps your panels and the data they show. The agent improves how they look, and how they're organized and sized on the dashboard.
- **Appearance and content** does the same, and can also change what the dashboard shows. The agent can add, change, replace, or remove panels, and add controls.

Restyling replaces any custom styling on your {{esql}} visualizations. Panels that the agent can't restyle, such as visualizations that don't use {{esql}}, keep their current look.

In both cases, the agent arranges panels using the best practices described in [Dashboard grid layout and best practices](arrange-panels.md#dashboard-grid-layout). You can apply the same practices when you arrange panels yourself.

## Discard the changes [enhance-dashboard-discard]

If you'd rather not keep the agent's changes, select **Reset changes** from the menu next to **Save**, before you save. Resetting returns the dashboard to its last saved version, so it also discards any unsaved edits of your own. Once you save, the changes become part of the dashboard, and you can no longer discard them in one step. To learn more, refer to [Reset dashboard changes](open-dashboard.md#reset-the-dashboard).

## Next steps [enhance-dashboard-next-steps]

- To enhance the dashboard again later, you don't need the **Enhance** button. While you edit the dashboard, open a new conversation and enter [`/dashboards`](/explore-analyze/ai-features/agent-builder/skills.md) followed by your request, for example `/dashboards Enhance this dashboard, appearance only`. If your request already says what to change, the agent skips the question and gets to work.
- To fine-tune the layout yourself, refer to [Organize dashboard panels](arrange-panels.md).

## Related pages [enhance-dashboard-related-pages]

- [Dashboards and visualizations in {{agent-builder}} chat](/explore-analyze/ai-features/agent-builder/agent-builder-dashboards-and-visualizations.md)
- [Create dashboards using AI](create-dashboards-using-ai.md)
- [`dashboards` skill](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-dashboard-management-skill)
