---
navigation_title: Create rules and action policies with Agent Builder
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How Agent Builder creates rules and action policies in the experimental alerting system using the rule management skill, what the agent produces, and the save-order dependency."
---

# Create rules and action policies with {{agent-builder}} [create-rules-action-policies-ai-agent]

Rule and action policy authoring in {{agent-builder}} is part of the {{alerting-v2-system}} in {{kib}}. The {{alerting-v2-system}} registers rules and action policies as attachment types in {{agent-builder}}, so an agent equipped with the rule management skill can propose, create, and configure them through natural language conversation.

Instead of filling out the rule form manually, you describe what you want to monitor and the agent uses its rule management skill and tools to resolve the data source and build a fully configured rule proposal for you.

## Propose and save a rule [ai-agent-rule-proposal]

To use this capability, open an agent in [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) that has the rule management skill configured. The rule management skill gives the agent domain expertise in {{alerting-v2-system}} rule authoring, including knowledge of ES\|QL query patterns, threshold configuration, grouping, and the alerting v2 data model. When you describe a monitoring requirement, the agent uses its tools to resolve the relevant data source and builds a rule proposal.

The proposal appears as an inline attachment in the conversation, summarizing the rule name, type, schedule, and tags. Opening the attachment shows the full configuration across three views:

- **Conditions** - The ES\|QL query, thresholds, grouping criteria, and schedule the agent constructed.
- **Query preview** - The results of running the proposed ES\|QL query against live data, so you can evaluate whether the rule would produce meaningful signal before committing to it.
- **Runbook** - A free-text runbook field associated with the rule, which the agent can populate from context in the conversation.

The agent can also search for and attach an existing rule to the conversation using the same inline attachment, opening the same view for inspection or revision.

The agent does not persist the rule automatically. Saving is an explicit action that signals the configuration is ready. Until the rule is saved, the proposal exists only in the conversation and is not evaluated against data.

:::{note} 
Signal rules do not support notifications. Alert episodes, and therefore action policies, only apply to rules running in Alert mode. If you ask the agent to set up notifications for a signal rule, the rule management skill explains the limitation and offers to either convert the rule to Alert mode or create a separate alert rule.
:::

## Example prompts [ai-agent-sample-prompts]

Use these prompts as a starting point, then adjust them to your data and thresholds:

- Create an error threshold rule on the checkout service data. Alert when there are more than 3 HTTP 5xx errors in the past 5 minutes, grouped by URL path.
- Monitor average CPU usage across all hosts. Alert when any host exceeds 90% for more than 10 minutes.
- Alert when log volume from the payments service drops below 100 events in a 5-minute window. This likely means data has stopped flowing.
- Set up a rule that tracks error rate by service. Alert at medium severity when the rate exceeds 1%, and critical when it exceeds 5%.


## Set up notifications [ai-agent-notification-setup]

After a rule is saved, you can ask the agent to configure notifications. The rule management skill handles this by creating two objects:

- A **workflow** - The delivery mechanism. It defines what happens when the {{alerting-v2-system}} determines that a notification should be sent: posting to Slack, emailing a team, triggering PagerDuty, and so on.
- An **action policy** - The gating mechanism. It evaluates alert episodes from the rule on a continuous schedule and invokes the workflow when the episode clears the policy's match conditions and frequency settings. When the agent creates an action policy alongside a specific rule, the policy is automatically scoped to that rule as a per-rule policy.

Both objects are proposed as inline attachments and must be explicitly saved before they take effect.

### Save order [save-order-ai-agent]

The three objects have a dependency chain that determines the order in which they must be saved:

1. **Rule** - The action policy references the rule by ID. The ID is not available until the rule is persisted.
2. **Workflow** - The action policy references the workflow as a destination. The reference must resolve to a persisted workflow.
3. **Action policy** - Can only be saved after both its rule and workflow dependencies exist.

This order is enforced in the UI. The action policy save control remains inactive until both dependencies are met.

## Related pages

- [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) - How the {{agent-builder}} platform works, including agents, skills, and tools.
<!-- - [About action policies](action-policies/about-action-policies.md) - How action policies evaluate and gate alert episodes before invoking a workflow. -->
<!-- - [Create an action policy](action-policies/create-configure-action-policy.md) - Configure a policy manually, with full control over type, match conditions, grouping, and destinations. -->
<!-- - [Connect workflows to the {{alerting-v2-system}}](workflows-alerting.md) - How action policies and lifecycle triggers invoke workflows at runtime, and when to use each. -->
