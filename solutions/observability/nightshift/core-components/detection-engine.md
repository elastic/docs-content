---
applies_to:
  serverless:
    observability: preview
description: Learn how the Elastic nightshift Detection engine learns your systems, generates and runs rules, and surfaces significant events as alerts.
products:
  - id: observability
  - id: cloud-serverless
---

# Detection engine [nightshift-detection-engine]

The Detection engine learns your systems, then tells you when something worth knowing has happened. It generates detection rules, runs them continuously, and surfaces a significant event when rule firings add up to something meaningful.

## From data to significant events [nightshift-detection-engine-flow]

Detection runs in the following phases. Each builds on the one before.

1. **Learn.** Elastic nightshift analyzes the data that detection watches and extracts [Knowledge Indicators](../significant-events/knowledge-indicators.md) (KIs). KIs are facts about your systems, such as the services that are running, the infrastructure they use, and how they depend on each other. For example, from a source's logs it extracts that the source contains a Python gRPC service called `recommendationservice` running on GKE.
1. **Generate rules.** Elastic nightshift converts KIs into {{esql}} rules that are scoped to the services and failure modes in your data. Rules can also be authored by people or installed by integrations.
1. **Run rules and detect.** Rules run on a schedule. Each rule produces signals and alerts. A separate step looks for statistically significant shifts in how often each rule fires.
1. **Discover.** The discovery agent looks across alerts, signals, raw data, and KIs to decide what matters. It verifies its own findings and opens a significant event when it confirms a problem. An event's status is active, recovering, or inactive.

KI extraction and rule generation prepare your sources for detection. After that, rule execution and discovery run continuously in the background. Detection requires an {{obs-serverless}} project on the Complete tier, and it uses the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md) for large language model (LLM) calls, so you don't need to configure an LLM connector or select a model. Refer to [Requirements](../get-started.md#nightshift-get-started-requirements).

## Rules, signals, alerts, and significant events [nightshift-detection-engine-terms]

A rule is a query that runs on a schedule against the data that detection watches. Rules come from three places:

- **Human-authored**: A person writes the rule.
- **Installed by integrations**: An integration provides the rule.
- **AI-driven**: Elastic nightshift generates the rule from the KIs it extracted.

Rules produce signals and alerts:

- A **signal** records a finding. Signals don't need to be acknowledged, assigned, or resolved.
- An **alert** has a lifecycle and needs action.
- A **significant event** is an alert that discovery creates. It brings together related evidence and context without a condition that you define. You can manage and route it like any other alert, and you can start an investigation from it.

On the **Detections** page, the **Events**, **Rules**, and **Signals** tabs show significant events, rules, and signals. An event's details list the detections behind it, each with the name of the rule that found it, the kind of change, and the entity that it applies to. Refer to [Audit and manage detections](../audit-and-manage-detections.md#nightshift-detections-review-events).

## Learn more [nightshift-detection-engine-nav]

- [Audit and manage detections](../audit-and-manage-detections.md): Set up and manage the data that detection watches, and review significant events
- [How Significant Events works](../significant-events/how-it-works.md): Learn the pipeline internals
- [Knowledge Indicators](../significant-events/knowledge-indicators.md): Learn how KIs work
- [Operator guide](../significant-events/operator-guide.md): Learn about system impact, cost drivers, and recovery
