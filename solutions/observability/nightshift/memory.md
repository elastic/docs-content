---
applies_to:
  serverless:
    observability: preview
description: Elastic nightshift context is a knowledge base of facts about your systems that investigations use to produce better results.
products:
  - id: observability
  - id: cloud-serverless
---

# Context engine [nightshift-memory]

The Elastic nightshift AI SRE uses a knowledge base of facts about your systems that agents read when investigating incidents. Rather than rebuilding an understanding of your environment from raw telemetry on every [investigation](./investigations.md), Elastic nightshift keeps knowledge about your services, infrastructure, dependencies, and known failure patterns, and uses it as a starting point.

:::{note}
Elastic nightshift isn't enabled by default. For what you need to use it, refer to [Requirements](./get-started.md#nightshift-get-started-requirements).
:::

## View what Elastic nightshift has learned [nightshift-memory-manage]

To see what Elastic nightshift knows about your systems, select {icon}`boxes_vertical` → **Knowledge**, then check the **Wiki** and **Memory** tabs:

- **Wiki**: Durable knowledge that the investigator reads before each run, organized into pages by type, such as services, runbooks, postmortems, and queries.
- **Memory**: Lessons that the investigator saves after a run and recalls when it works on a similar problem, such as how a previous problem was resolved or which checks found its cause.

Elastic nightshift manages the Wiki and Memory itself, so you can't edit them. To stop Elastic nightshift from using something that isn't correct or useful, archive it. You can restore it later. To give Elastic nightshift more context about your systems and processes, add instructions to an automation. For the steps, refer to [Manage knowledge and memory](./manage/manage-knowledge-and-memory.md).

## How investigations use context [nightshift-memory-usage]

When an [investigation](./investigations.md) starts, the investigation agent reads the knowledge relevant to the affected services before querying your telemetry. This means the agent starts with an understanding of your environment, and investigations produce more accurate conclusions than they would from raw data alone.

Elastic nightshift also learns from the investigations it runs. It saves what it learns to the Wiki and Memory, which makes later investigations more accurate and uses fewer tokens. If something it learned isn't correct, archive it.

## Give feedback [nightshift-memory-feedback]

Use the **Submit feedback** {icon}`comment` button at the top of the page to share your experience. Your feedback goes directly to the team.

## Learn more [nightshift-memory-nav]

- [Manage knowledge and memory](./manage/manage-knowledge-and-memory.md): Review what Elastic nightshift has learned and give it context
- [Get started with Elastic nightshift](./get-started.md): Check the requirements, enable Elastic nightshift, and run your first investigation
- [Core components](./core-components/index.md): Learn how the engines, automations, and connectors work
- [Work in Elastic nightshift](./work-in-elastic-nightshift.md): Investigate and respond, audit and manage detections, and automate investigations