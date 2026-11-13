---
applies_to:
  serverless:
    observability: preview
description: Learn how Elastic nightshift works, including its Context, Detection, and Investigation engines, automations, and connectors.
products:
  - id: observability
  - id: cloud-serverless
---

# Core components [nightshift-core-components]

Elastic nightshift is made up of three engines that work together, plus the automations and connectors that connect them to your team and your tools.

## How Elastic nightshift works [nightshift-how-it-works]

Elastic nightshift finds problems in your systems, investigates them, and proposes fixes. Three engines do the work, and people stay in control of what happens next.

## The flow [nightshift-how-it-works-flow]

1. **Learn your systems.** The [Context engine](../memory.md) holds what Elastic nightshift knows about your systems, such as which services are running and how they depend on each other.
1. **Detect problems.** The [Detection engine](./detection-engine.md) watches your data. When rule firings add up to something meaningful, it surfaces a significant event. A significant event is an alert, so you can manage and route it like any other alert.
1. **Start an investigation.** An investigation starts from an alert, a significant event, a problem you describe, or an [automation](./automations.md).
1. **Find the cause.** The [Investigation engine](../investigations.md) gathers evidence from your data and from the context, tests hypotheses, and reports a conclusion.
1. **Propose actions.** The investigation ends with [proposed actions](../investigations.md#nightshift-investigation-engine-proposed-actions), which are changes that you can make to mitigate or fix the problem.

## Where people stay in control [nightshift-how-it-works-people]

- You or an automation start investigations. Elastic nightshift doesn't start an investigation on its own beyond the automations that you set up.
- You make the changes that proposed actions describe, and then confirm that you did. Elastic nightshift doesn't carry them out.
- You review what Elastic nightshift knows about your systems, archive what isn't useful, and give it context through automation instructions.
- You choose which connectors investigations can use. Refer to [Connectors and integrations](./connectors-and-integrations.md).

## Learn more [nightshift-core-components-nav]

- [Context engine](../memory.md): Learn how Elastic nightshift stores and uses knowledge about your systems
- [Detection engine](./detection-engine.md): See how Elastic nightshift goes from your data to significant events
- [Investigation engine](../investigations.md): Learn how an investigation goes from an alert to proposed actions
- [Automations](./automations.md): Learn how automations pull alerts into investigations and post results
- [Connectors and integrations](./connectors-and-integrations.md): See the external systems that investigations use

To use Elastic nightshift day to day, refer to [Work in Elastic nightshift](../work-in-elastic-nightshift.md).
