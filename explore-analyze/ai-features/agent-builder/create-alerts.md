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
OPEN (#4): {{kib}} alerting rule availability may vary by serverless project type (Search, Observability, Security). Confirm before asserting serverless: ga on specific steps (@meghanmurphy1).
Do not publish any ES|QL query that has not been run on a 9.5 cluster. Mark examples "test on your own data".
-->

{{agent-builder}} records what each agent does as OpenTelemetry traces in your own {{es}} cluster. Because these traces capture token usage, error status, span durations, and tool calls, you can use {{kib}} alerting rules to be notified when something needs attention, such as a cost spike or a failing tool. There is no separate alerting interface. You create standard {{kib}} rules against the trace data stream.

<!-- TODO intro: keep it short. Name the four things you can alert on: per-conversation token spikes, token cost or budget over time, agent error-rate spikes, and repeated tool failures. -->

## Prerequisites

* Trace collection is turned on. <!-- TODO(#7322): link to Collect traces (collect-traces.md) once it is on main. -->
* Read access to the trace data streams. See [Permissions](permissions.md). <!-- TODO(#7322): point to the #read-trace-data anchor once #7322 adds it. -->
* {{kib}} alerting access and a connector for notifications, such as Slack, email, or PagerDuty. See [Set up alerting](/explore-analyze/alerting/alerts/alerting-setup.md).

<!-- Do not re-explain the data streams, privacy settings, or the access model. Link to collect-traces.md and permissions.md instead. -->

## Create a rule

Use an [{{es}} query rule](/explore-analyze/alerting/alerts/rule-type-es-query.md) with ES|QL to alert on the trace data stream. For a simple numeric threshold, an [index threshold rule](/explore-analyze/alerting/alerts/rule-type-index-threshold.md) is an alternative.

<!-- TODO: confirm the exact rule types available, and on which serverless project types, on a 9.5 cluster. -->

1. Create a rule. <!-- TODO: exact navigation path. See /explore-analyze/alerting/alerts/create-manage-rules.md -->
2. Select the {{es}} query rule type and use ES|QL.
3. Target the trace data stream for your space: `traces-agent_builder.otel-<space-id>`. <!-- Avoid wildcards. Scope one space per rule. -->
4. Define the condition. <!-- See the examples below. -->
5. Set the check schedule. <!-- The blog example checks every 15 minutes. -->
6. Add an action and a connector.

## Example alerts

<!--
Write each example as a condition plus the specific fields it uses. Pull only the fields each alert needs and link to the dashboard page (#7170) for the full reference. Do not duplicate the reference.
Field reference (verify against #7170 before publishing; may shift with the OTel schema upgrade search-team#15270 / kibana#277640):
- Tokens: attributes.gen_ai.usage.input_tokens, attributes.gen_ai.usage.output_tokens on `chat *` spans.
- Errors: status.code == "Error".
- Tools: span.name LIKE "execute_tool *", tool name = bare `name`.
- Agent executions: span.name LIKE "invoke_agent *" + attributes.elastic.inference.span.kind == "AGENT", grouped by attributes.gen_ai.agent.id.
Mark every query "test on your own data". Do not publish an untested query.
-->

### A conversation exceeds a token limit

<!--
Sum input_tokens + output_tokens on `chat *` spans, grouped by conversation.
OPEN (#2): conversation IDs are hashed by default unless agentBuilder:tracing:realIds is on. Verify the grouping field (the blog uses labels.conversation_id, which is not in the verified #7170 reference) and note the privacy dependency, or alert on aggregate token volume instead.
OPEN (#3): confirm the example threshold stays under the conversation token limit (Chat team). The blog settled on 256,000.
TODO: add tested ES|QL.
-->

### Token consumption over a period exceeds a budget

<!-- Sum tokens on `chat *` spans over a time window and compare to a budget. TODO: add tested ES|QL. -->

### An agent's error rate spikes

<!-- Ratio of status.code == "Error" on invoke_agent AGENT spans, grouped by attributes.gen_ai.agent.id, over a window. TODO: add tested ES|QL. -->

### A specific tool fails repeatedly

<!--
Count execute_tool * spans with status.code == "Error", grouped by the bare `name` field, over a window.
OPEN (#1): status.code == "Error" captures thrown or validation errors only, such as invalid parameters, not errors a tool returns (search-team#15284, kibana#277689). Document this limitation or scope the example. TODO: add tested ES|QL and the limitation note.
-->

## Related

<!-- TODO(#7322): Collect traces (collect-traces.md) -->
<!-- TODO(#7337): Agent Builder traces dashboard (agent-traces-dashboard.md), full span and attribute reference -->
* [Create and manage rules](/explore-analyze/alerting/alerts/create-manage-rules.md)
* [{{es}} query rule](/explore-analyze/alerting/alerts/rule-type-es-query.md)
