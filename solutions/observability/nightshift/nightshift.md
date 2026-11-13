---
applies_to:
  serverless:
    observability: preview
description: Learn what Elastic nightshift is, why you'd use it, how it works, and where to start.
products:
  - id: observability
  - id: cloud-serverless
---

# {{nightshift}} [nightshift-overview]

{{nightshift}} is an AI site reliability engineer (SRE) available in {{product.serverless-observability}}. When something goes wrong in production, it investigates for you by querying your logs, metrics, and traces, reading your code if you connect it, testing explanations, and providing a likely cause with evidence and proposed actions. You decide what happens next.

It learns your system as it works, and brings that knowledge to every investigation, chat, and detection. It can also watch your data for problems that none of your alerts catch.

**If this is your first time**, [Get started](./get-started.md) takes you from enabling {{nightshift}} to your first investigation in a few steps.

:::{image} ../../images/nightshift-home.png
:alt: The Elastic nightshift home page, with investigations grouped by severity, including High investigations about inventory-api latency and Postgres lock timeouts
:screenshot:
:::

## Why use {{nightshift}} [nightshift-overview-why]

Knowledge of how your system fits together usually sits with a few engineers. A new SRE has the skills but not the knowledge, and AI models start with the same gap. {{nightshift}} builds that knowledge as it works, so it starts with the problem instead of learning your system.

{{nightshift}} does the first pass of an incident, so you start from a summary instead of a blank dashboard. Investigations work using your existing data and alerts you already, without detection turned on: no re-instrumenting, no rewritten rules. Here are some common situations and how they play out with and without {{nightshift}}:

| Situation | Without {{nightshift}} | With {{nightshift}} |
| --- | --- | --- |
| An alert fires | You piece together what changed from dashboards and traces. | An automation investigates it. You open the likely cause and evidence. |
| Something is wrong, but no alert fired | Users or a teammate tell you. | Detections group unusual changes into a significant event. |
| The cause is in the code | You search your repositories for the change. | {{nightshift}} reads the relevant code and pull requests in a temporary sandbox, without copying or indexing them. |
| Your team works in Slack | You copy charts and links into the channel. | You mention `@Elastic`, and the results appear in the thread. |
| A problem comes back | You have to find someone who remembers the previous solution. | {{nightshift}} starts with context from previous investigations. |

## How it works [nightshift-overview-how]

:::{image} ../../images/nightshift-how-it-works.svg
:alt: How an investigation flows from a trigger, through detection and context, to the proposed actions you decide on.
:::

1. **An investigation starts.** The trigger can be a question, an `@Elastic` mention in Slack, selecting **Investigate** on an alert or significant event, or an automation.
1. **{{nightshift}} investigates.** It queries your data, reads connected code, and tests hypotheses, ranked by confidence.
1. **It uses and builds context.** It reads its Wiki and Memory first to get context, and saves what it learns.
1. **It proposes actions.** It provides a likely cause, the evidence, proposed actions, and what it was unsure of.
1. **You decide.** {{nightshift}} never changes your environment. You apply or decline each action. Administrators set run limits and can pause detection in [Settings and limits](./settings.md).

Conclusions can be wrong. Before you act, check the reasoning in the hypothesis tree. Refer to [How investigations work](./investigation/index.md#nightshift-investigations-accuracy).

## What it costs [nightshift-overview-cost]

{{nightshift}} is billed by the model tokens it uses, and daily run limits keep spending predictable. Refer to [Cost and models](./cost-and-models.md).

## Availability [nightshift-overview-availability]

{{nightshift}} is available on {{obs-serverless}} projects on the Complete tier, in the default space only. Refer to [Known issues](./known-issues.md).

## Give feedback [nightshift-feedback]

On the {{nightshift}} home page, open the {icon}`boxes_vertical` menu and select **Feedback**.

## Learn more [nightshift-overview-start]

- [Get started](./get-started.md): Set up {{nightshift}} and run your first investigation.
- [Investigate anything](./use-cases/investigate-anything.md): Ask about any problem, in your own words.
- [Investigate in Slack](./use-cases/investigate-in-slack.md): Ask for help from a Slack channel.
- [Investigate your alerts](./use-cases/investigate-alerts.md): Find out why an alert fired.
- [Automatically investigate your alerts](./use-cases/auto-investigate-alerts.md): Set up an [automation](./investigation/automations.md) to investigate alerts before you look at them.
- [Detect problems automatically](./use-cases/detect-problems.md): Find problems that none of your alerts catch with [detection](./detection/index.md), an optional add-on.
- [How investigations work](./investigation/index.md): Read an investigation and check its reasoning.
- [How context is built](./context/index.md): Review or correct what {{nightshift}} learned in the Wiki, Memory, and Knowledge Indicators.
- [Cost and models](./cost-and-models.md): Find out what {{nightshift}} costs and how your data is used.
- [Reference architecture](./reference-architecture.md): Check what works with your deployment, whether {{serverless-short}}, {{ech}}, or self-managed.
