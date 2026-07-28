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


When Nightshift surfaces a critical Significant Event, it automatically triggers an investigation. For lower-severity events, you can trigger one manually using the **Run investigation** button on the event. The investigation attempts to determine the root cause and propose remediation options by running as a background workflow against your streams data and connected tools.

## How investigations work [nightshift-investigations-how]

Each investigation runs as a structured, agentic process:

1. **Memory read** — Before querying raw telemetry, the investigation agent reads relevant [memory pages](nightshift-memory.md) about your system. If Nightshift has previously encountered similar issues or has context about the affected service, it uses that knowledge as a starting point.

2. **Targeted queries** — The agent runs targeted ES|QL queries against your streams to gather evidence about the event — error rates, service dependencies, infrastructure state, and related signals.

3. **External tool calls** — If external connectors are configured (such as GitHub, Slack, or cloud provider APIs), the agent calls those tools to gather additional context, such as recent deployments, open incidents, or code changes.

4. **Hypothesis and remediation** — The agent synthesizes all evidence into a root cause hypothesis with a confidence assessment. It also proposes ranked remediation options where it can determine them.

6. **Memory write-back** — New findings — such as failure patterns or service relationships discovered during the investigation — are written back to [memory](nightshift-memory.md) so future investigations benefit from this context.

## What an investigation produces [nightshift-investigations-output]

A completed investigation provides:

- **Hypotheses** — Ranked root cause candidates, each with a confidence percentage. The leading hypothesis reflects what the investigation determined most likely.
- **Conclusion** — The determined root cause with supporting evidence, including specific log counts, error patterns, and any source code or external signal that confirmed the finding.
- **Next steps** — Specific, actionable items. These are textual suggestions only — Nightshift does not take automated remediation actions.
- **Gaps found** — Data sources or access boundaries Nightshift couldn't reach during the investigation, such as missing structured log fields, unavailable infrastructure metrics, or connectors with limited access. Gaps are listed explicitly so you know what the investigation couldn't verify.

## Where to view investigations [nightshift-investigations-viewing]

### From the Nightshift landing page [nightshift-investigations-landing-page]

Each Significant Event on the [landing page](nightshift-landing-page.md) shows its investigation status. Click the event to open the detail view, then expand the **Investigation** section to see results.

### From chat [nightshift-investigations-chat]

Click **Chat** on any Significant Event to open an AI conversation with the investigation context pre-attached. You can:

- Read the full investigation narrative.
- Ask follow-up questions about specific evidence.
- Request alternative hypotheses.
- Explore remediation options in more depth.

## Triggering investigations [nightshift-investigations-triggering]

Nightshift automatically triggers an investigation for every critical Significant Event. For lower-severity events, use the **Run investigation** button on the event to trigger one manually.

## Investigation states [nightshift-investigations-states]

| State | Meaning |
|-------|---------|
| **Running** | The investigation agent is actively gathering evidence and building its hypothesis. |
| **Completed** | The investigation has finished and results are available. |

## Relationship to memory [nightshift-investigations-memory]

Investigations and [memory](nightshift-memory.md) form a feedback loop: investigations read memory to start from a richer baseline, and write new findings back to memory when they're done. Over time, this means investigations for recurring issue types become progressively faster and more accurate as Nightshift accumulates knowledge about your environment.

## Learn more [nightshift-investigations-nav]

- [Nightshift overview](./nightshift.md)
- [Investigations](./investigations.md)
- [Memory](./memory.md)
