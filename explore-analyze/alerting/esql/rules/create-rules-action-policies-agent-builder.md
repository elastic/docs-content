---
navigation_title: Create rules using Agent Builder
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Create Universal Alerting rules and action policies with Agent Builder. Describe what to monitor in natural language, review the proposal, and save the rule, workflow, and action policy."
---

# Create rules and action policies with {{agent-builder}} [create-rules-agent-builder]

Use {{agent-builder}} to create and configure {{alerting-v2-system}} rules and action policies through natural language instead of the rule form. Describe what you want to monitor, and an agent equipped with the [`rule-authoring`](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-rule-authoring-skill) skill (`rule-management` in 9.5) resolves the data source and proposes a fully configured rule.

## Requirements [create-ai-agent-requirements]

Before you start, make sure you have the following:

- **The required subscription** - {{agent-builder}} requires the appropriate {{stack}} [subscription](https://www.elastic.co/pricing) or {{serverless-short}} [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-features-add-ons).
- {applies_to}`stack: experimental =9.5` **The `agentBuilder:experimentalFeatures` advanced setting turned on** - Go to the **Advanced Settings** menu using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and turn on `agentBuilder:experimentalFeatures`.
- {applies_to}`stack: experimental =9.5` **To search for and edit existing rules and action policies, the `contextEngine:enabled` advanced setting also turned on** - Turn it on in the same way, in each space where you use the agent.
- {applies_to}`stack: experimental 9.6+` {applies_to}`serverless: experimental` **To search for existing rules and action policies from a conversation, the `agentBuilder:experimentalFeatures` advanced setting turned on** - Without it, the agent can still create rules and action policies. It can also edit a saved rule or action policy when you open the agent from that rule's details page or that policy's edit page. To turn it on, refer to [Enable experimental features](/explore-analyze/ai-features/agent-builder/get-started.md#enable-experimental-features-optional).
- {applies_to}`stack: experimental 9.6+` **A space that uses the Classic or {{observability}} solution view** - The `rule-authoring` and `action-policy-authoring` skills aren't available in other spaces.
- {applies_to}`serverless: experimental` **An {{obs-serverless}} project** - The `rule-authoring` and `action-policy-authoring` skills aren't available in other project types.
- **The required privileges** - Your role needs the [privileges to use {{agent-builder}} and save rules and action policies](../manage/configure-access.md#alerting-agent-builder-privileges).

## Propose and save a rule [ai-agent-rule-proposal]

### Start a proposal [ai-agent-start-proposal]

To create a rule, go to **Alerting** → **Rules** in the {{observability}} navigation menu, or find **Rules** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

Then select the creation path that lets you create the rule with an agent. Alternatively, open any agent in [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) that has the [`rule-authoring`](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-rule-authoring-skill) skill configured.

The `rule-authoring` skill gives the agent domain expertise in {{alerting-v2-system}} rule authoring, including knowledge of {{esql}} query patterns, threshold configuration, grouping, and the {{alerting-v2-system}} data model. When you describe a monitoring requirement, the agent uses its tools to resolve the relevant data source and builds a rule proposal.

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

After you save a rule, you can ask the agent to configure notifications. The agent proposes the workflows and action policies needed to deliver them.

{applies_to}`stack: experimental =9.5` The `rule-management` skill creates the action policies itself.

{applies_to}`stack: experimental 9.6+` {applies_to}`serverless: experimental` The [`action-policy-authoring`](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-action-policy-authoring-skill) skill creates action policies. After the `rule-authoring` skill proposes a complete rule that opens alerts, it offers to set up notifications. If you accept, the agent loads `action-policy-authoring`.

:::{note}
Action policies invoke workflows for alerts only. If you ask the agent to set up notifications for a rule that doesn't open alerts, it explains the limitation and offers a way forward:

- **Unsaved rule** - The agent changes the draft rule so that it opens alerts. Then you save the rule.
- **Saved rule** - Whether a rule opens alerts can't change after you save it, so the agent offers to create a new rule with the same query and schedule that does, and to set up notifications on that one.
:::

- **Workflows** - Workflows are the delivery mechanism. They define what happens when {{alerting-v2-system}} determines that a notification should be sent, such as posting to Slack, emailing a team, triggering PagerDuty, and so on.
- **Action Policies** - Action policies are the gating mechanism. {{kib}} evaluates them against the rule's alerts and invokes the workflow for the alerts they apply to. When you create an action policy with a rule, the policy applies to that rule's alerts.
    * {applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.6+` The agent links the policy to the rule with a [routing tag](../action-policies/create-configure-action-policy.md#routing-tags). If the rule already has a routing tag that no other rule uses, the agent can reuse it. Otherwise, the agent adds a `notify-<rule-name>` routing tag to the rule and the policy, in lowercase with hyphens (for example, `notify-high-cpu-prod`). The policy also applies to alerts from any other rule with that routing tag. If the agent adds a routing tag to a rule you already saved, save the rule again so the tag takes effect.
    * {applies_to}`stack: removed 9.6+, experimental =9.5` {applies_to}`serverless: unavailable` The action policy references the rule by ID.

Both objects are proposed as inline attachments and must be explicitly saved before they take effect.

### Save order [save-order-ai-agent]

The three objects depend on each other. Save them in this recommended order:

1. **Rule** - Save the rule first. The link between the rule and the action policy takes effect only after the rule is saved.
2. **Workflow** - The action policy references the workflow as a destination. The reference must resolve to a persisted workflow.
3. **Action policy** - Save the action policy last.
    * {applies_to}`stack: experimental 9.6+` {applies_to}`serverless: experimental` You can't save the action policy until its workflow exists: {{kib}} disables **Create policy** while a workflow destination is still a draft. You can save the policy before the rule, but the policy doesn't apply to the rule's alerts until the rule is saved.
    * {applies_to}`stack: experimental =9.5` You can't save the action policy until both its rule and its workflow exist.

:::{note}
:applies_to: {"stack": "removed 9.6+, experimental =9.5", "serverless": "unavailable"}
Action policies saved or edited through {{agent-builder}} also receive the `agent-builder-assisted` tag automatically, with the same behavior: user-editable and re-applied on subsequent agent edits.
:::

## Related pages

- [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md): Learn how the {{agent-builder}} platform works, including agents, skills, and tools.
- [About action policies](../action-policies/about-action-policies.md): Understand the gating mechanism the agent configures on your behalf.
- [Connect workflows to {{alerting-v2-system}}](../workflows-alerting.md): Understand the delivery mechanism the agent sets up when you ask it to configure notifications.
