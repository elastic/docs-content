---
description: "Find what the AlertZero Attack Discovery Worker does in Elastic Security, how it hands attacks to forensics, and its limits."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-attack-discovery}} {{az-worker}}

The {{az-attack-discovery}} {{az-worker}} groups related alerts into candidate attacks, then checks each one before it reaches you. It's part of the [{{az-triage-watch}}](triage-watch.md), and it runs the [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) feature of {{elastic-sec}} on a schedule.

It opens one {{az-investigation}} for each candidate attack, or adds the attack to an open {{az-investigation}} for the same attack, then judges whether the attack is a false positive. For a false positive, it acknowledges the open alerts and closes the {{az-investigation}}. For an attack it confirms or can't rule out, it proposes handing the attack to the [{{az-forensics-watch}}](forensics-watch.md) for forensics.

It has only the [settings every {{az-worker}} has](../watches-and-workers.md#alertzero-shared-worker-settings). By default, it runs every 24 hours, and each run picks up where the last one ended. It offers {{az-manual}} and {{az-supervised}} {{az-autonomy}}. Refer to [what it does at each level](../watches-and-workers.md#alertzero-worker-autonomy-levels).

## Limits [alertzero-attack-discovery-limits]

* Each run retrieves up to 10,000 alerts for every 24 hours it covers.
* You can't [run it on demand](../run-worker-on-demand.md).

## Work with this {{az-worker}} [alertzero-attack-discovery-tasks]

- **Before you turn it on:** Check [what it needs](../requirements.md).
- **Decide its work:** Its {{az-proposed-actions}} appear in the **Investigate** section of the **{{az-proposed-actions-cap}}** page. Refer to [](../respond-to-attack.md).
- **Change its settings:** Refer to [](../configure-worker-settings.md).
