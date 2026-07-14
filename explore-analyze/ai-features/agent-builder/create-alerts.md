---
navigation_title: "Create alerts on trace data"
description: "Create Kibana alerting rules on Agent Builder trace data to monitor token usage, costs, agent error rates, and tool failures."
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

<!--
How-to (docs-content#7173). Last page in the trace cluster.
Depends on #7171 (trace collection, PR #7322) and reuses the field reference from #7170 (dashboard, PR #7337).
Lifecycle drafted GA 9.5 (Stack and Serverless), matching the trace cluster.
RESOLVED (#4): The Elasticsearch query rule and index threshold rule are both serverless: ga Stack rules, and Agent Builder runs on the Elasticsearch (Search) serverless project type, so serverless: ga is supportable for the steps. Spot-check on a 9.5 Elasticsearch serverless project that both rule types appear in Create rule (Stack Management > Rules).
Do not publish any ES|QL query that has not been run on a 9.5 cluster. Mark examples "test on your own data".
-->

{{agent-builder}} collects execution traces into a data stream in your own {{es}} cluster. These traces record token usage, errors, latency, and tool calls, so you can create {{kib}} alerting rules that notify you when something needs your attention. For example, you can alert on a conversation that uses too many tokens, token costs that exceed a budget, an agent error rate that spikes, or a tool that fails repeatedly.

{{agent-builder}} has no dedicated alerting interface. You create standard {{kib}} rules against the trace data stream, so the rule types, check schedules, and connectors are the same ones you use elsewhere in {{kib}}.

## Prerequisites

Before you create a rule, make sure that:

* **Trace collection is on.** {{agent-builder}} must be writing traces to the `traces-agent_builder.otel-<space-id>` data stream in the space where you create the rule. Collection is on by default. <!-- TODO(#7322): link to Collect traces (collect-traces.md) once it is on main. -->
* **You can read the trace data.** The rule queries `traces-agent_builder.otel-*`, so you need read access to those data streams. See [Permissions](permissions.md). <!-- TODO(#7322): update to the #read-trace-data anchor once #7322 adds it. -->
* **You can use {{kib}} alerting.** You need privileges to create and manage rules, plus a connector to send notifications such as Slack, email, or PagerDuty. See [Set up alerting](/explore-analyze/alerting/alerts/alerting-setup.md).

## Create a rule

Alert on the trace data with an [{{es}} query rule](/explore-analyze/alerting/alerts/rule-type-es-query.md) that runs an ES|QL query on a schedule and runs an action when the query returns matches. For a simple numeric threshold, you can use an [index threshold rule](/explore-analyze/alerting/alerts/rule-type-index-threshold.md) instead.

With ES|QL, the query targets the data stream directly in its `FROM` command, so you do not need a data view. The alert condition lives in the query, usually in a `WHERE` clause that compares a value to a threshold. Query one space at a time and avoid wildcards, so you do not mix data from different spaces.

1. In {{kib}}, go to **{{stack-manage-app}}** > **{{rules-ui}}** and click **Create rule**.
2. Select the **{{es}} query** rule type, then enter a name and optional tags.
3. For the query language, select **ES|QL**.
4. Enter your ES|QL query against the trace data stream for your space, for example `FROM traces-agent_builder.otel-<space-id>`. The query defines the condition, including the threshold. See [Example alerts](#example-alerts).
5. Set the alert grouping:

    * **Time field**: the field used to filter results by the rule's time window, for example `@timestamp`.
    * **Alert group**: select **Create an alert for each row** to raise one alert per matching row, for example per conversation over the threshold. Select **Create an alert if matches are found** to raise a single alert when the query returns any rows.
6. Set the **time window** to define how far back the query searches, for example the last hour.
7. Set the **check interval** to define how often the rule runs. Keep it smaller than the time window to avoid gaps in detection.
8. Click **Test query** to confirm the query is valid. For an ES|QL query, the matching rows appear in a table.
9. Add an action, select a connector, then set the action frequency. See [Add actions](/explore-analyze/alerting/alerts/rule-type-es-query.md#_add_actions).
10. Click **Save**.

:::{note}
ES|QL rules do not offer the **Exclude matches from previous run** option. If the check interval is smaller than the time window, a row that keeps matching can alert more than once. Choose the time window, check interval, and query so that a condition alerts as often as you want.
:::

After you save the rule, it appears on the **{{rules-ui}}** page, where you can confirm that it runs on schedule and check its status.

<!-- TODO(cluster): confirm the navigation path to the Rules page on BOTH a 9.5 Stack deployment and an Elasticsearch Serverless project. If it differs, use an applies-switch. Confirm the ES|QL query language option and the "Create an alert for each row" / "Create an alert if matches are found" labels appear as written in 9.5. -->
<!-- TODO(cluster): run Test query against real trace data and confirm it returns the expected rows. Confirm the healthy rule status label shown on the Rules page (for example "Succeeded" or "Active") and update the last sentence to match. -->
<!-- TODO(screenshot, optional): decide whether to add one screenshot of the rule form with a trace ES|QL query and its Test query results. Screenshots are optional in how-tos and add maintenance cost. -->

## Example alerts

Each example gives an ES|QL query and the rule settings to use with it. Adjust the fields, thresholds, and time windows to your environment.

:::{note}
These queries are starting points, not tested rules. Run each one with **Test query** on your own data before you rely on it. Replace `default` in `traces-agent_builder.otel-default` with your space id. The rule applies its own time window through the **Time field** you select, so the queries do not include a `@timestamp` filter.
:::

<!-- TODO(cluster): validate every query below on 9.5 trace data. Confirm the field names (attributes.gen_ai.usage.input_tokens / output_tokens, attributes.gen_ai.conversation.id, attributes.gen_ai.agent.id, attributes.elastic.inference.span.kind, span.name, status.code, name), that TO_LONG is needed before SUM, and that the rule applies the time window via the Time field so no @timestamp filter is needed in the query. If a manual filter IS required, add `| WHERE @timestamp >= NOW() - <window>` to each query. -->

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

256,000 is an example cost threshold, not a hard limit. {{agent-builder}} compacts long conversations, so a conversation can pass this value without failing. By default, `attributes.gen_ai.conversation.id` is a stable hash, which is enough to group and count conversations. To show the real conversation ID in alerts, turn on `agentBuilder:tracing:includeRealIds`.

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
| EVAL is_error = CASE(status.code == "Error", 1, 0)
| STATS executions = COUNT(*), errors = SUM(is_error) BY attributes.gen_ai.agent.id
| EVAL error_rate = TO_DOUBLE(errors) / executions
| WHERE executions >= 20 AND error_rate > 0.1
```

Rule settings:

* **Alert group**: Create an alert for each row, so you get one alert per agent.
* **Time window**: the period to evaluate, for example the last hour.

The `executions >= 20` guard avoids noisy alerts when an agent has run only a few times. `error_rate > 0.1` alerts when more than 10 percent of executions fail.

<!-- TODO(cluster): confirm that invoke_agent AGENT spans carry status.code == "Error" when an agent execution fails, and that this is the right span for an agent error rate. If agent errors are not recorded here, measure errors on a different span (for example chat spans) and update this query. -->

### A specific tool fails repeatedly

Alert when a tool records more than a set number of errors. Count `execute_tool` spans with an error status and group by tool name.

```esql
FROM traces-agent_builder.otel-default
| WHERE `span.name` LIKE "execute_tool *" AND status.code == "Error"
| STATS failures = COUNT(*) BY name
| WHERE failures > 5
```

Rule settings:

* **Alert group**: Create an alert for each row, so you get one alert per tool.
* **Time window**: the period to evaluate, for example the last hour.

:::{note}
In 9.5, `status.code == "Error"` on `execute_tool` spans captures thrown and validation errors, such as invalid parameters. It might not capture an error that a tool returns as a normal result, so this alert can miss some tool failures.
:::

<!-- TODO(author): when kibana#277689 (search-team#15284) merges and backports to 9.5, returned tool errors also set status.code == "Error" and add attributes.error.type = "tool_error". Revisit the note above and consider using attributes.error.type. -->

## Related

<!-- TODO(#7322): Collect traces (collect-traces.md) -->
<!-- TODO(#7337): Agent Builder traces dashboard (agent-traces-dashboard.md), full span and attribute reference -->
* [Create and manage rules](/explore-analyze/alerting/alerts/create-manage-rules.md)
* [{{es}} query rule](/explore-analyze/alerting/alerts/rule-type-es-query.md)
