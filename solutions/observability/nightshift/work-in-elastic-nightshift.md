---
applies_to:
  serverless:
    observability: preview
description: Choose the Elastic nightshift task that you need, from investigating and responding to problems and auditing detections to setting up automations.
products:
  - id: observability
  - id: cloud-serverless
---

# Work in Elastic nightshift [nightshift-use]

Elastic nightshift finds problems in your systems, investigates them, and proposes fixes. These pages cover what you do with it day to day: investigating problems, reviewing what detection found, and automating investigations. For how each part works, refer to [Core components](./core-components/index.md).

## How the pieces fit together [nightshift-use-flow]

1. The [Detection engine](./core-components/detection-engine.md) watches your data and surfaces significant events, which are alerts.
1. You start an investigation from an alert, a significant event, or a problem that you describe.
1. An [automation](./core-components/automations.md) can start investigations for you, so you don't start each one yourself.
1. You review the investigation's results, make the changes that its [proposed actions](./investigations.md#nightshift-investigation-engine-proposed-actions) describe, and mark them as applied.

## Choose a task [nightshift-use-tasks]

| Task | What you do |
|---|---|
| [Investigate and respond](./investigate-and-respond.md) | Find what needs attention, start an investigation from an alert, a significant event, or a problem you describe, read the results, act on proposed actions, and ask follow-up questions in chat or Slack. |
| [Audit and manage detections](./audit-and-manage-detections.md) | Choose the data that detection watches, manage your sources, and review the significant events that detection found. |
| [Set up an automation](./set-up-an-automation.md) | Set up automatic investigations that start when an alert fires, a Slack message arrives, or on a schedule, and post the results to Slack. |
