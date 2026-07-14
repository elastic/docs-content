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

Use an [{{es}} query rule](/explore-analyze/alerting/alerts/rule-type-es-query.md) with ES|QL to alert on the trace data stream. For a simple numeric threshold, an [index threshold rule](/explore-analyze/alerting/alerts/rule-type-index-threshold.md) is an alternative.

<!-- RESOLVED (#4): Elasticsearch query rule (ES|QL) and index threshold rule are both serverless: ga. On serverless, create rules from Stack Management > Rules. Spot-check availability on a 9.5 Elasticsearch serverless project before publishing. -->

1. Create a rule. <!-- TODO: exact navigation path. See /explore-analyze/alerting/alerts/create-manage-rules.md -->
2. Select the {{es}} query rule type and use ES|QL.
3. Target the trace data stream for your space: `traces-agent_builder.otel-<space-id>`. <!-- Avoid wildcards. Scope one space per rule. -->
4. Define the condition. <!-- See the examples below. -->
5. Set the check schedule. <!-- The blog example checks every 15 minutes. -->
6. Add an action and a connector.

## Example alerts

<!--
Write each example as a condition plus the specific fields it uses. Pull only the fields each alert needs and link to the dashboard page (#7170) for the full reference. Do not duplicate the reference.
Field reference (verified 2026-07-13 vs Kibana source and the shipped traces skill):
- Tokens: attributes.gen_ai.usage.input_tokens, attributes.gen_ai.usage.output_tokens, on `chat *` spans only. Wrap in TO_LONG(...) before SUM.
- Conversation id: attributes.gen_ai.conversation.id (present on every span in the trace, including chat spans). NOT labels.conversation_id.
- Errors: status.code == "Error".
- Tools: span.name LIKE "execute_tool *", tool name = bare `name`.
- Agent executions: span.name LIKE "invoke_agent *" + attributes.elastic.inference.span.kind == "AGENT", grouped by attributes.gen_ai.agent.id.
OTel schema upgrade (search-team#15270 / kibana#277640, v9.5.0) does NOT rename any of these trace fields; only the value casing of gen_ai.provider.name normalizes to lowercase, and message content moves to new attributes in the logs stream (not used here). Re-verify lightly before publish.
Mark every query "test on your own data". Do not publish an untested query.
-->

### A conversation exceeds a token limit

<!--
Sum input_tokens + output_tokens on `chat *` spans (wrap each in TO_LONG before SUM), grouped by attributes.gen_ai.conversation.id.
RESOLVED (#2): the grouping field is attributes.gen_ai.conversation.id, NOT labels.conversation_id (the blog is wrong). Conversation IDs are hashed by default, but the hash is stable, so per-conversation grouping still works. The setting agentBuilder:tracing:includeRealIds (default false) exposes the real UUID. Add a short privacy note; this alert does not need the real IDs.
RESOLVED (#3): keep 256,000 as the example. There is no hard token cap that rejects a conversation (Agent Builder auto-compacts long conversations), so frame the alert as cost and length monitoring, not crash prevention. The Chat team chose 256,000 as a cost breakpoint.
TODO: add tested ES|QL.
-->

### Token consumption over a period exceeds a budget

<!-- Sum tokens on `chat *` spans over a time window and compare to a budget. TODO: add tested ES|QL. -->

### An agent's error rate spikes

<!-- Ratio of status.code == "Error" on invoke_agent AGENT spans, grouped by attributes.gen_ai.agent.id, over a window. TODO: add tested ES|QL. -->

### A specific tool fails repeatedly

<!--
Count execute_tool * spans with status.code == "Error", grouped by the bare `name` field, over a window.
RESOLVED (#1): in 9.5, status.code == "Error" on execute_tool * captures thrown or validation errors only (for example invalid parameters), and may NOT catch errors a tool returns as a normal result. The fix (search-team#15284 / kibana#277689) is still a draft with no 9.5 or backport label as of 2026-07-13, so document the limitation for 9.5. Do NOT reference attributes.error.type yet; it only exists once that PR merges. Add a clear limitation note next to this example. TODO: add tested ES|QL.
-->

## Related

<!-- TODO(#7322): Collect traces (collect-traces.md) -->
<!-- TODO(#7337): Agent Builder traces dashboard (agent-traces-dashboard.md), full span and attribute reference -->
* [Create and manage rules](/explore-analyze/alerting/alerts/create-manage-rules.md)
* [{{es}} query rule](/explore-analyze/alerting/alerts/rule-type-es-query.md)
