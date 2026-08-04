---
applies_to:
  stack: experimental 9.5
  serverless: experimental
description: Nightshift autonomous investigations analyze Significant Events to determine root cause, assess blast radius, and propose remediation options without manual intervention.
products:
  - id: observability
  - id: cloud-serverless
---

# Investigations [nightshift-investigations]


An investigation is a background workflow that reads memory pages, queries your streams data, and calls connected external tools to determine the root cause of a Significant Event and propose remediation options. Results include ranked root cause hypotheses with confidence scores, a conclusion with supporting evidence, and actionable next steps.

When Nightshift surfaces a `critical` or `high` severity Significant Event, it automatically triggers an investigation. For lower-severity events, you can trigger one manually using the **Run investigation** button on the event.

## How investigations work [nightshift-investigations-how]

Each investigation runs as a structured, agentic process:

- **Memory read**: Before querying raw telemetry, the investigation agent reads relevant [memory pages](./memory.md) about your system. If Nightshift has previously encountered similar issues or has context about the affected service, it uses that knowledge as a starting point.

- **Targeted queries**: The agent runs targeted ES|QL queries against your streams to gather evidence about the event — error rates, service dependencies, infrastructure state, and related signals.

- **External tool calls**: If external connectors are configured (such as GitHub, Slack, or cloud provider APIs), the agent calls those tools to gather additional context, such as recent deployments, open incidents, or code changes.

- **Hypothesis and remediation**: The agent synthesizes all evidence into a root cause hypothesis with a confidence assessment. It also proposes ranked remediation options where it can determine them.

- **Memory write-back**: New findings — such as failure patterns or service relationships discovered during the investigation — are written back to [memory](./memory.md) so future investigations benefit from this context.

## View investigations [nightshift-investigations-viewing]

You can view investigations in the Nightshift UI or chat with the AI Agent.

### From the Nightshift UI [nightshift-investigations-landing-page]

Each Significant Event on the [landing page](./nightshift.md) shows its investigation status. Select the event to open the details view, then expand the **Investigation** section to see results.

### From chat [nightshift-investigations-chat]

Select **Open in chat** on any Significant Event to open an AI conversation with the investigation context pre-attached. You can:

- Read the full investigation narrative.
- Ask follow-up questions about specific evidence.
- Request alternative hypotheses.
- Explore remediation options in more depth.

## What an investigation produces [nightshift-investigations-output]

A completed investigation provides:

- **Hypotheses**: Ranked root cause candidates, each with a confidence percentage. The leading hypothesis reflects what the investigation determined most likely.
- **Conclusion**: The determined root cause with supporting evidence, including specific log counts, error patterns, and any source code or external signal that confirmed the finding.
- **Next steps**: Specific, actionable items. These are textual suggestions only — Nightshift does not take automated remediation actions.
- **Gaps found**: Data sources or access boundaries Nightshift couldn't reach during the investigation, such as missing structured log fields, unavailable infrastructure metrics, or connectors with limited access. Gaps are listed explicitly so you know what the investigation couldn't verify.

## Give feedback [nightshift-investigations-feedback]

Use the **Submit feedback** {icon}`comment` button at the top of the page to share your experience. Your feedback goes directly to the team.

## Learn more [nightshift-investigations-nav]

- [Nightshift overview](./nightshift.md): Get an overview of Nightshift, requirements, and how to get started
- [Memory](./memory.md): Learn how Nightshift stores and uses system knowledge to improve investigation quality over time
- [How Significant Events works](../streams/significant-events/how-it-works.md): Pipeline internals for KI extraction, rule generation, detection, and discovery
- [Knowledge Indicators](../streams/significant-events/knowledge-indicators.md): Get an in-depth overview of how KIs work
- [Operator guide](../streams/significant-events/operator-guide.md): Learn more about system impact, cost drivers, and operational procedures