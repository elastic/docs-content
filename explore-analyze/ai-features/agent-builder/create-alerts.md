---
navigation_title: "Create alerts on trace data"
description: "Create Kibana alerting rules on Agent Builder trace data to monitor token usage, agent error rates, and tool failures."
applies_to:
  stack: ga 9.5+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Create alerts on {{agent-builder}} trace data

{{agent-builder}} collects execution traces into a data stream in your {{es}} cluster. These traces record token usage, errors, latency, and tool calls, so you can create {{kib}} alerting rules that notify you when something needs your attention. For example, you can alert on a conversation that uses too many tokens, total token usage that exceeds a budget, an agent error rate that spikes, or a tool that fails repeatedly.

Because traces are stored in a regular data stream, you can use the same {{kib}} rule types, check schedules, and connectors as any other alerting workflow.

## Prerequisites

Before you create a rule, make sure that:

* **Trace collection is on.** {{agent-builder}} must be writing traces to the `traces-agent_builder.otel-<space-id>` data stream in the space where you create the rule. Collection is on by default. <!-- TODO(#7322): link to Collect traces (collect-traces.md) once it is on main. -->
* **You can read the trace data.** The rule queries `traces-agent_builder.otel-*`, so you need read access to those data streams. See [Permissions](permissions.md). <!-- TODO(#7322): update to the #read-trace-data anchor once #7322 adds it. -->
* **You can use {{kib}} alerting.** You need privileges to create and manage rules, plus a connector to send notifications such as Slack, email, or PagerDuty. See [Set up alerting](/explore-analyze/alerting/alerts/alerting-setup.md).

## Create a rule

Alert on the trace data with an [{{es}} query rule](/explore-analyze/alerting/alerts/rule-type-es-query.md) that runs an ES|QL query on a schedule and runs an action when the query returns matches.

:::{tip}
For a simple count-based threshold, you can use an [index threshold rule](/explore-analyze/alerting/alerts/rule-type-index-threshold.md) instead. It cannot sum the token fields, so use the {{es}} query rule with ES|QL for token-based alerts.
:::

With ES|QL, the query targets the data stream directly in its `FROM` command, so you do not need a data view. The alert condition lives in the query, usually in a `WHERE` clause that compares a value to a threshold. Query one space at a time and avoid wildcards, so you do not mix data from different spaces.

1. In {{kib}}, go to **{{stack-manage-app}}** → **{{rules-ui}}** and click **Create rule**.
2. Select the **{{es}} query** rule type, then name the rule.
3. For the query language, select **ES|QL**.
4. Enter your ES|QL query against the trace data stream for your space, for example `FROM traces-agent_builder.otel-<space-id>`. The query defines the condition, including the threshold. See [Example alerts](#example-alerts).
5. Set the alert grouping:

    * **Select a time field**: the field used to filter results by the rule's time window, for example `@timestamp`.
    * **Select alert group**: select **Create an alert for each row** to raise one alert per matching row, for example per conversation over the threshold. Select **Create an alert if matches are found** to raise a single alert when the query returns any rows.
6. Set the **time window** to define how far back the query searches, for example the last hour.
7. Set the **check interval** to define how often the rule runs. Keep it smaller than the time window to avoid gaps in detection.

    :::{note}
    ES|QL rules do not offer the **Exclude matches from previous run** option. If the check interval is smaller than the time window, a row that keeps matching can alert more than once. Choose the time window, check interval, and query so that a condition alerts as often as you want.
    :::
8. Click **Test query** to confirm the query is valid. For an ES|QL query, the matching rows appear in a table.
9. Add an action, select a connector, then set the action frequency. See [Add actions](/explore-analyze/alerting/alerts/rule-type-es-query.md#_add_actions).
10. Click **Save**.

After you save the rule, it appears on the **{{rules-ui}}** page, where you can confirm that it runs on schedule and check its status.

## Example alerts

Each example gives an ES|QL query and the rule settings to use with it. Adjust the fields, thresholds, and time windows to your environment.

:::{note}
These queries are starting points, not tested rules. Run each one with **Test query** on your own data before you rely on it. Replace `default` in `traces-agent_builder.otel-default` with your space id. The rule applies its own time window through the **Time field** you select, so the queries do not include a `@timestamp` filter. If you run a query outside a rule, make sure a time range applies, through the {{kib}} time picker or a `@timestamp` filter in the query, so it does not scan the whole data stream.
:::

:::{note}
By default, {{agent-builder}} anonymizes custom tool names, so any query that groups by tool name buckets all custom tools under `execute_tool custom`. Built-in tools keep their names. To group by individual custom tool names, turn on **Include real tool and agent names in traces** (`agentBuilder:tracing:includeRealNames`).
:::

### A conversation exceeds a token limit

Alert when a single conversation uses more than a set number of tokens. Sum the input and output tokens on the conversation's `chat` spans and group by conversation.

```esql
FROM traces-agent_builder.otel-default
| WHERE `span.name` LIKE "chat *"
| STATS input_tokens = SUM(TO_LONG(attributes.gen_ai.usage.input_tokens)),
        output_tokens = SUM(TO_LONG(attributes.gen_ai.usage.output_tokens))
    BY attributes.gen_ai.conversation.id
| EVAL total_tokens = input_tokens + output_tokens
| WHERE total_tokens > 256000
```

Rule settings:

* **Alert group**: Create an alert for each row, so you get one alert per conversation over the threshold.
* **Time window**: the period to evaluate, for example the last 24 hours.

256,000 is an example token threshold, not a hard limit. {{agent-builder}} compacts long conversations, so a conversation can pass this value without failing. By default, `attributes.gen_ai.conversation.id` is a stable hash, which is enough to group and count conversations. To include the real conversation ID in alerts, turn on the **Include real conversation and workflow IDs** privacy setting (`agentBuilder:tracing:includeRealIds`).

### Token consumption over a period exceeds a budget

Alert when total token usage across all conversations goes over a budget for the period. This is the same sum without grouping by conversation.

```esql
FROM traces-agent_builder.otel-default
| WHERE `span.name` LIKE "chat *"
| STATS input_tokens = SUM(TO_LONG(attributes.gen_ai.usage.input_tokens)),
        output_tokens = SUM(TO_LONG(attributes.gen_ai.usage.output_tokens))
| EVAL total_tokens = input_tokens + output_tokens
| WHERE total_tokens > 5000000
```

Rule settings:

* **Alert group**: Create an alert if matches are found, so you get a single alert for the period.
* **Time window**: the budget period, for example the last 30 days.

Set the threshold to your budget. 5,000,000 is a placeholder.

### An agent's error rate spikes

Alert when an agent's error rate goes above a threshold. Count each agent's executions and its errors, then compare the ratio.

```esql
FROM traces-agent_builder.otel-default
| WHERE `span.name` LIKE "invoke_agent *" AND attributes.elastic.inference.span.kind == "AGENT"
| STATS executions = COUNT(*), errors = COUNT(*) WHERE status.code == "Error"
    BY attributes.gen_ai.agent.id
| EVAL error_rate = TO_DOUBLE(errors) / executions
| WHERE executions >= 20 AND error_rate > 0.1
```

Rule settings:

* **Alert group**: Create an alert for each row, so you get one alert per agent.
* **Time window**: the period to evaluate, for example the last hour.

The `executions >= 20` guard avoids noisy alerts when an agent has run only a few times. `error_rate > 0.1` alerts when more than 10 percent of executions fail. Like conversation IDs, `attributes.gen_ai.agent.id` is a stable hash by default, so custom agents group by hash unless you turn on `agentBuilder:tracing:includeRealIds`.

This alert counts agent executions that fail outright. An error that the agent handles and still returns as a completed response does not set `status.code` to `Error`, so it is not counted here.

### A specific tool fails repeatedly

Alert when a tool records more than a set number of errors. Count `execute_tool` spans that have an error status and group by the tool's span name.

```esql
FROM traces-agent_builder.otel-default
| WHERE `span.name` LIKE "execute_tool *" AND status.code == "Error"
| STATS failures = COUNT(*) BY `span.name`
| WHERE failures > 5
```

Rule settings:

* **Alert group**: Create an alert for each row, so you get one alert per tool.
* **Time window**: the period to evaluate, for example the last hour.

Each alert identifies the tool by its span name, for example `execute_tool <toolId>`.

:::{note}
{applies_to}`stack: ga 9.5`

`status.code == "Error"` on `execute_tool` spans is set only for parameter and schema validation errors, such as invalid arguments. Errors that a tool catches and returns as a result do not set this status, so this alert can miss some tool failures.
:::

<!-- TODO(author): kibana#277689 (returned tool errors also set status.code == "Error" and add attributes.error.type = "tool_error") merged for 9.6 with backport:skip, so it is NOT in 9.5. The 9.5 note above stays correct. Revisit this when documenting 9.6. -->

## Related

% RE-ADD the two links below once their target pages are on main. Remove the leading "% " from each link line.
% Re-add when PR #7322 merges (collect-traces.md lands on main):
% * [Collect traces](collect-traces.md): turn on trace collection and learn about the data streams, privacy settings, and access model.
% Re-add when PR #7337 merges (agent-traces-dashboard.md lands on main):
% * [Agent Builder traces dashboard](agent-traces-dashboard.md): the prebuilt overview dashboard and the full span and attribute reference.
* [Monitor usage and costs](monitor-usage.md): how {{agent-builder}} counts tokens and how usage maps to cost.
* [Create and manage rules](/explore-analyze/alerting/alerts/create-manage-rules.md): manage, snooze, and troubleshoot {{kib}} alerting rules.
* [{{es}} query rule](/explore-analyze/alerting/alerts/rule-type-es-query.md): full reference for the rule type used on this page.
