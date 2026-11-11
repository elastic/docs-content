---
applies_to:
  serverless:
    observability: preview
description: Elastic nightshift provides automated investigations and on-call assistance for Elastic Observability, triggered from your alerts and significant events.
products:
  - id: observability
  - id: cloud-serverless
---

# Elastic nightshift AI SRE

Elastic nightshift AI SRE is built into {{observability}} to find and investigate production problems alongside your team. It learns your systems, watches your data for significant events, and runs investigations that gather evidence and test hypotheses, so your team spends less time sorting through noise and more time on the decisions that need a person.

An investigation can start from an alert, a significant event, or a problem you describe, or an automation can start it for you when an alert fires or on a schedule. Each investigation ends with proposed actions, such as a command to run, a configuration change, or a rollback. Each comes with the evidence and conclusion behind it, so you can check the reasoning before you make the change.

Three engines work together to detect problems in your systems and investigate them:

| Engine | What it does |
| --- | --- |
| [Detection engine](./core-components/detection-engine.md) | Learns your systems, then tells you when something worth knowing has happened. It extracts [Knowledge Indicators](./significant-events/knowledge-indicators.md) from your data, such as which services are running, what infrastructure they use, and how they depend on each other. It generates detection rules from them and runs those rules continuously. When rule firings add up to something meaningful, it surfaces a [significant event](./core-components/detection-engine.md#nightshift-detection-engine-terms) as an alert, so you can manage and route it like any other Elastic alert. |
| [Investigation engine](./investigations.md) | Works out what's behind an alert. You can start an investigation from an alert, a significant event, or the home page. The investigation gathers evidence from your data and from what Elastic nightshift knows about your systems, determines the likely cause, and reports its findings with proposed actions. |
| [Context engine](./memory.md) | The shared knowledge layer the other engines draw on. It stores what Elastic nightshift knows about your systems, including the Knowledge Indicators that detection produces, and makes that knowledge available when an investigation starts. You can review that knowledge, archive what isn't useful, and give Elastic nightshift more context through automation instructions. |

For how the engines work together, refer to [How Elastic nightshift works](./core-components/index.md#nightshift-how-it-works).

## The home page [nightshift-landing-page]

The home page is the central view of your investigations. It groups them by severity so you can see what's being investigated and what needs your attention. From it, you can start an investigation, open an investigation to read its findings, and reach knowledge and settings. Refer to [Review what needs attention](./investigate-and-respond.md#nightshift-investigations-attention).

## Give feedback [nightshift-feedback]

Use the **Submit feedback** {icon}`comment` button at the top of the page to share your experience. Your feedback goes directly to the team.

## Learn more [nightshift-landing-page-nav]

- [Get started](./get-started.md): Check the requirements, enable Elastic nightshift, connect your tools, and run your first investigation
- [Core components](./core-components/index.md): Learn how the engines, automations, and connectors work
- [Work in Elastic nightshift](./work-in-elastic-nightshift.md): Investigate and respond, audit and manage detections, and automate investigations
- [Manage Elastic nightshift](./manage/index.md): Configure settings, control access, manage knowledge, and set run limits
