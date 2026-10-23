---
applies_to:
  serverless:
    observability: preview
description: Elastic nightshift context is a knowledge base of facts about your systems that investigations use to produce better results.
products:
  - id: observability
  - id: cloud-serverless
---

# Context [nightshift-memory]

The Elastic nightshift AI SRE uses a knowledge base of facts about your systems that agents read when investigating incidents. Rather than rebuilding an understanding of your environment from raw telemetry on every [investigation](./investigations.md), Elastic nightshift keeps knowledge about your services, infrastructure, dependencies, and known failure patterns, and uses it as a starting point.

:::{note}
Elastic nightshift is in private preview and isn't enabled by default. To request access, contact your Elastic account team.
:::

## View and edit context [nightshift-memory-manage]

To see what Elastic nightshift knows about your systems, select {icon}`boxes_vertical` → **Knowledge**, then check the **Cortex** and **Memory** tabs:

- **Cortex**: Durable knowledge that the investigator reads before each run, organized into pages by type, such as services, runbooks, postmortems, and queries.
- **Memory**: Lessons that the investigator saves after a run and recalls when it works on a similar problem, such as how a previous problem was resolved or which checks found its cause.

Review the knowledge to confirm it's correct for your environment. You can edit, archive, or delete anything that isn't correct or useful. You can also add information about your systems and processes that Elastic nightshift might not discover from your data, such as team conventions, deployment processes, or known issues. For the steps, refer to [Manage what Elastic nightshift knows about your systems](./get-started.md#nightshift-get-started-knowledge).

## How investigations use context [nightshift-memory-usage]

When an [investigation](./investigations.md) starts, the investigation agent reads the knowledge relevant to the affected services before querying your telemetry. This means the agent starts with an understanding of your environment, and investigations produce more accurate conclusions than they would from raw data alone.

Elastic nightshift also learns from every investigation it runs. It saves what it learns as knowledge, which makes later investigations more accurate and uses fewer tokens. If something it learned isn't correct, you can edit, archive, or delete it.

## Give feedback [nightshift-memory-feedback]

Use the **Submit feedback** {icon}`comment` button at the top of the page to share your experience. Your feedback goes directly to the team.

## Learn more [nightshift-memory-nav]

- [Get started with Elastic nightshift](./get-started.md): Start an investigation and review the results
- [Elastic nightshift](./nightshift.md): Get an overview of Elastic nightshift and its requirements
- [Investigations](./investigations.md): Learn how Elastic nightshift investigates problems and how to read the results
- [How Significant Events works](./significant-events/how-it-works.md): Pipeline internals for KI extraction, rule generation, detection, and discovery
- [Knowledge Indicators](./significant-events/knowledge-indicators.md): Get an in-depth overview of how KIs work
- [Operator guide](./significant-events/operator-guide.md): Learn more about system impact, cost drivers, and operational procedures
