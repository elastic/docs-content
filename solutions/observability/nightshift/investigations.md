---
applies_to:
  serverless:
    observability: preview
description: Learn how the Elastic nightshift Investigation engine works out what's behind an alert, what starts an investigation, how it runs, and what it produces.
products:
  - id: observability
  - id: cloud-serverless
---

# Investigation engine [nightshift-investigation-engine]

The Investigation engine works out what's behind an alert. An investigation is an automated analysis of an issue in your systems. When an investigation runs, Elastic nightshift AI SRE gathers evidence from your data and from what it already knows about your systems, then reports what happened, what likely caused it, and what to look at next.

## What starts an investigation [nightshift-investigation-engine-triggers]

An investigation can start in the following ways:

- **You describe a problem.** Start a manual investigation from the Elastic nightshift home page.
- **An alert or alert episode.** Start an investigation from an alert, or from an alert episode from the [{{alerting-v2-system}}](/explore-analyze/alerting/esql/system-overview.md).
- **A significant event.** Start an investigation from the details of a significant event that the [Detection engine](./core-components/detection-engine.md) surfaced.
- **An automation.** An automation starts an investigation when an alert fires, on a schedule, or from a Slack message. Refer to [Automations](./core-components/automations.md).

If you start an investigation from an alert or significant event that's already part of an open investigation, Elastic nightshift adds to that investigation instead of opening a second one. Each new alert starts its own investigation, even when it comes from the same rule. A closed investigation is never continued.

For the steps, refer to [Start an investigation](./investigate-and-respond.md#nightshift-investigations-start).

## How investigations work [nightshift-investigation-engine-how]

Each investigation runs as an agentic process in the background, in a sandbox:

- **Context first**: The investigation agent starts from what Elastic nightshift knows about your systems, such as the services involved, their dependencies, and any context you've given it through automation instructions. Refer to [Context engine](./memory.md).
- **Evidence gathering**: The agent runs targeted queries against your data to collect evidence about the problem and the services it affects. It reaches your data and tools through connectors. Refer to [Connectors and integrations](./core-components/connectors-and-integrations.md).
- **Findings**: The agent synthesizes what it found into a conclusion about the likely root cause.
- **Learning**: The agent saves what it learned about your systems to the Wiki and Memory, so future investigations are more accurate and use fewer tokens. Refer to [Context engine](./memory.md).

## What an investigation produces [nightshift-investigation-engine-output]

A completed investigation shows what happened, what it affects, and the best-supported explanation for why it occurred. It includes a hypothesis tree that shows the hypotheses the investigation tested, and it ends with proposed actions that you can take to mitigate or fix the problem. Each investigation has a severity, which the home page uses to group investigations.

To read the results, refer to [Read the results](./investigate-and-respond.md#nightshift-investigations-results).

## Proposed actions [nightshift-investigation-engine-proposed-actions]

A proposed action is a change that an investigation suggests to mitigate or fix a problem. Every investigation ends with proposed actions, each with a title and an explanation of why Elastic nightshift suggests it. A proposed action can be:

- A command to run
- A configuration change
- A code fix
- A rollback
- A suggestion to gather more information

Elastic nightshift doesn't carry out proposed actions. You make the change in your environment, then confirm in the investigation that you did. If an action doesn't suit your system, you can decline it. In the hypothesis tree, each proposed action has a **High confidence**, **Medium confidence**, or **Low confidence** label.

To review an action, refer to [Review proposed actions](./investigate-and-respond.md#nightshift-investigations-actions).

## Learn more [nightshift-investigation-engine-nav]

- [Investigate and respond](./investigate-and-respond.md): Start an investigation and work with its results
- [Context engine](./memory.md): Learn how Elastic nightshift stores and uses knowledge about your systems
- [How Elastic nightshift works](./core-components/index.md#nightshift-how-it-works): See where the Investigation engine fits in
