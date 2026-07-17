---
navigation_title: Create rules using Agent Builder
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How Agent Builder creates rules and action policies in the experimental alerting system using the rule management skill, what the agent produces, and the save-order dependency."
---

# Create rules and action policies with {{agent-builder}} [create-rules-agent-builder]

Use {{agent-builder}} to create and configure rules and action policies through natural language instead of the rule form. Describe what you want to monitor, and an agent equipped with the rule management skill resolves the data source and proposes a fully configured rule.

## Requirements [create-ai-agent-requirements]

Before you start, make sure you have the following:

- **The required subscription** - {{agent-builder}} requires the appropriate {{stack}} [subscription](https://www.elastic.co/pricing) or {{serverless-short}} [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-features-add-ons).
- **The `agentBuilder:experimentalFeatures` advanced setting turned on** - Go to the **Advanced Settings** menu using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and turn on `agentBuilder:experimentalFeatures`.
- **The required privileges** - Your [role](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) must include the following:

  | To... | Required privilege |
  |---|---|
  | Access and use {{agent-builder}} | **{{agent-builder}}: Read** (under **Analytics**) |
  | Save the rule | **Rules: All** (under **Alerting**) |
  | Save the action policy | **Action Policies: All** (under **Alerting**) |
  | Select or create the workflow destination | **Workflows: Read** to select an existing workflow; **Workflows: All** to create one (under **Analytics > Workflows**) |

## Propose and save a rule [ai-agent-rule-proposal]

### Start a proposal [ai-agent-start-proposal]

To create a rule, go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Rules**. When choosing a creation path, select the one that lets you create the rule with an agent. Alternatively, open any agent in [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) that has the rule management skill configured. 

The rule management skill gives the agent domain expertise in {{alerting-v2-system}} rule authoring, including knowledge of {{esql}} query patterns, threshold configuration, grouping, and the {{alerting-v2-system}} data model. When you describe a monitoring requirement, the agent uses its tools to resolve the relevant data source and builds a rule proposal.

### Review the proposal [ai-agent-review-proposal]

The proposal appears as an inline attachment in the conversation, summarizing the rule name, type, schedule, and tags. Opening the attachment shows the full configuration across three views:

- **Conditions** - The {{esql}} query, thresholds, grouping criteria, and schedule the agent constructed.
- **Query preview** - The results of running the proposed {{esql}} query against live data, so you can evaluate whether the rule would produce meaningful signal before committing to it.
- **Runbook** - A free-text runbook field associated with the rule, which the agent can populate from context in the conversation.

The agent can also search for and attach an existing rule to the conversation using the same inline attachment, opening the same view for inspection or revision.

### Save the rule [ai-agent-save-rule]

The agent does not persist the rule automatically. Saving is an explicit action that signals the configuration is ready. Until the rule is saved, the proposal exists only in the conversation and is not evaluated against data.

When {{agent-builder}} saves or edits a rule, {{kib}} automatically adds an `agent-builder-assisted` tag to it. The tag appears on the **Rules** page and works as a normal filter tag. You can remove it or edit it manually. If the agent edits the same rule later, the tag is re-applied automatically.

## Example prompts [ai-agent-sample-prompts]

Use these prompts as a starting point, then adjust them to your data and thresholds:

- Create an error threshold rule on the checkout service data. Alert when there are more than 3 HTTP 5xx errors in the past 5 minutes, grouped by URL path.
- Monitor average CPU usage across all hosts. Alert when any host exceeds 90% for more than 10 minutes.
- Alert when log volume from the payments service drops below 100 events in a 5-minute window. This likely means data has stopped flowing.
- Set up a rule that tracks error rate by service. Alert at medium severity when the rate exceeds 1%, and critical when it exceeds 5%.

## Set up notifications [ai-agent-notification-setup]

After a rule is saved, you can ask the agent to configure notifications. The rule management skill handles this by creating workflows and action policies.

:::{note}
Signal rules do not support notifications. Alert episodes, and therefore action policies, only apply to rules running in Alert mode. If you ask the agent to set up notifications for a signal rule, the rule management skill explains the limitation and offers to either convert the rule to Alert mode or create a separate alert rule.
:::

- **Workflows** - Workflows are the delivery mechanism. They define what happens when the {{alerting-v2-system}} determines that a notification should be sent, such as posting to Slack, emailing a team, triggering PagerDuty, and so on.
- **Action policies** - Action policies are the gating mechanism. They evaluate alert episodes from the rule on a continuous schedule and invoke the workflow when the episode clears the action policy's match conditions and frequency settings. When the agent creates an action policy alongside a specific rule, the action policy is automatically scoped to that rule.

Both objects are proposed as inline attachments and must be explicitly saved before they take effect.

### Save order [save-order-ai-agent]

The three objects have a dependency chain that determines the order in which they must be saved:

1. **Rule** - The action policy references the rule by ID. The ID is not available until the rule is persisted.
2. **Workflow** - The action policy references the workflow as a destination. The reference must resolve to a persisted workflow.
3. **Action policy** - Can only be saved after both its rule and workflow dependencies exist.

Action policies saved or edited through {{agent-builder}} also receive the `agent-builder-assisted` tag automatically, with the same behavior: user-editable and re-applied on subsequent agent edits.

## Related pages

- [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) - How the {{agent-builder}} platform works, including agents, skills, and tools.
<!-- - [About action policies](action-policies/about-action-policies.md) - How action policies evaluate and gate alert episodes before invoking a workflow. -->
<!-- - [Create an action policy](action-policies/create-configure-action-policy.md) - Configure an action policy manually, with full control over match conditions, grouping, and destinations. -->
<!-- - [Connect workflows to the {{alerting-v2-system}}](workflows-alerting.md) - How action policies and lifecycle triggers invoke workflows at runtime, and when to use each. -->
