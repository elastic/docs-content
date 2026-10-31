---
description: "Find what the AlertZero Attack Discovery Worker does, what it needs, its settings, and where its work appears in Elastic Security."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-attack-discovery}} {{az-worker}}

The {{az-attack-discovery}} {{az-worker}} belongs to the [{{az-triage-watch}}](triage-watch.md). It groups related alerts into candidate attacks, then checks each one before it reaches you. It runs the [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) feature of {{elastic-sec}} on a schedule.

It opens one {{az-investigation}} for each candidate attack, or adds the attack to an open {{az-investigation}} for the same attack, then judges whether the attack is a false positive. For a false positive, it acknowledges the open alerts and closes the {{az-investigation}}. For an attack it confirms or can't rule out, it proposes handing the attack to the [{{az-forensics-watch}}](forensics-watch.md) for forensics.

## Requirements [alertzero-attack-discovery-requirements]

The {{az-attack-discovery}} {{az-worker}} needs detection alerts, and Attack Discovery workflows (`securitySolution:enableAttackDiscoveryWorkflows`) turned on in the space. To hand attacks off, [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) must be on too (the `contextEngine:enabled` advanced setting). Both are off by default. To get those attacks analyzed, turn on the [{{az-endpoint-analysis}} {{az-worker}}](endpoint-analysis-worker.md) too. Refer to [{{az-worker}} dependencies](../requirements.md).

## Settings [alertzero-attack-discovery-settings]

The {{az-attack-discovery}} {{az-worker}} has no settings beyond {{az-autonomy}}, **Trigger**, and **Models**. Find them on the {{az-triage-watch}} page. To change them, refer to [](../configure-worker-settings.md).

**{{az-autonomy-cap}}**
:   How much it does without waiting for you. At either level, it closes false positives on its own. Default: {{az-manual}}.

    * **{{az-manual}}**: Every handoff to the {{az-forensics-watch}} waits for your approval.
    * **{{az-supervised}}**: It hands attacks off without waiting for you.

**Trigger**
:   How often it runs, in minutes, hours, or days. Each run picks up where the last one ended.

    Default: every 24 hours.

**Models**
:   A link to **Feature Settings**, where you select the models that {{alertzero}} uses in the space.

## Where its work appears [alertzero-attack-discovery-work]

Its {{az-proposed-actions}} appear in the **Investigate** section of the **{{az-proposed-actions-cap}}** page. Refer to [](../respond-to-attack.md).

## Limits [alertzero-attack-discovery-limits]

* Each run retrieves up to 10,000 alerts for every 24 hours it covers.
* You can't [run it on demand](../run-worker-on-demand.md).
