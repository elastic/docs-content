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

The {{az-attack-discovery}} {{az-worker}} is part of the [{{az-triage-watch}}](triage-watch.md). It groups related alerts into candidate attacks and checks each one before it reaches you. This page explains when to use the {{az-attack-discovery}} {{az-worker}}, what data it needs, how it finds and checks attacks, where to decide its {{az-proposed-actions}}, and which limits apply.

## When to use the {{az-attack-discovery}} {{az-worker}} [alertzero-attack-discovery-when-to-use]

The {{az-attack-discovery}} {{az-worker}} is the right fit when:

* You want the {{az-attack-discovery}} {{az-worker}} to connect related alerts into attacks, instead of piecing them together yourself.
* You want the {{az-attack-discovery}} {{az-worker}} to check each candidate attack for false positives before it reaches you.
* You want the [{{az-forensics-watch}}](forensics-watch.md) to investigate confirmed attacks on an affected host.

The {{az-attack-discovery}} {{az-worker}} isn't the best fit when:

* Most of your alerts are false positives. Turn on the [{{az-alert-triage}} {{az-worker}}](alert-triage-worker.md) first, so the {{az-attack-discovery}} {{az-worker}} analyzes fewer, more meaningful alerts.
* Your space generates far more than 10,000 alerts in 24 hours. Each time the {{az-attack-discovery}} {{az-worker}} runs, it retrieves up to 10,000 alerts for each 24-hour period since its previous run, so reduce alert volume first.

## Data requirements [alertzero-attack-discovery-data]

The {{az-attack-discovery}} {{az-worker}} needs detection alerts in the space with a status of open or acknowledged. It skips building block alerts and alerts closed as false positives.

## How it works [alertzero-attack-discovery-how-it-works]

On each run, the {{az-attack-discovery}} {{az-worker}}:

1. Runs the [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) feature of {{elastic-sec}} on open and acknowledged alerts to find candidate attacks.
2. Opens one {{az-investigation}} for each candidate attack, or adds the attack to an open {{az-investigation}} for the same attack.
3. Judges whether each attack is a false positive.
4. For a false positive, acknowledges the open alerts and closes the attack and the {{az-investigation}}. For an attack it confirms or can't rule out, proposes handing the attack to the [{{az-forensics-watch}}](forensics-watch.md) for forensics.

Because the {{az-attack-discovery}} {{az-worker}} analyzes only open and acknowledged alerts, it skips any alert that the [{{az-alert-triage}} {{az-worker}}](alert-triage-worker.md) closed as a false positive.

You review the {{az-attack-discovery}} {{az-worker}}'s {{az-proposed-actions}} in the **Investigate** section of the **{{az-proposed-actions-cap}}** page. To learn how to take an attack from the {{az-attack-discovery}} {{az-worker}}'s verdict to containment, refer to [](../respond-to-attack.md).

### Example [alertzero-attack-discovery-example]

Over one day, alerts fire on the same host for a suspicious PowerShell command, a new scheduled task, and an outbound connection to a rarely seen domain. The {{az-attack-discovery}} {{az-worker}} groups the alerts into one candidate attack and opens an {{az-investigation}}. It can't rule the attack out, so it proposes handing the attack to the {{az-forensics-watch}}. After you approve, the [{{az-endpoint-analysis}} {{az-worker}}](endpoint-analysis-worker.md) investigates the host.

% After elastic/docs-content#9114 merges, consider adding this Worker's Context Engine requirement to Data requirements, with a link to ../set-up-alertzero.md#alertzero-turn-on-workers.

## Settings [alertzero-attack-discovery-settings]

**Trigger**
:   How often the {{az-attack-discovery}} {{az-worker}} runs.

    Default: Every 24 hours. Each time the {{az-attack-discovery}} {{az-worker}} runs, it starts where its previous run ended.

**{{az-autonomy-cap}}**
:   How much the {{az-attack-discovery}} {{az-worker}} does without you. You can set it to **{{az-manual}}** or **{{az-supervised}}**. Refer to [what it does at each level](../configure-worker-settings.md#alertzero-worker-autonomy).

    Default: {{az-manual}}

**Models**
:   Opens **Feature settings**, where you select the models that {{alertzero}} uses in the space. The {{az-attack-discovery}} {{az-worker}} has no model setting of its own, so it uses the models you select there.

% Link the model recommendations page once it exists: For help choosing models, refer to [](../model-recommendations.md).

## Limits [alertzero-attack-discovery-limits]

* Each time the {{az-attack-discovery}} {{az-worker}} runs, it retrieves up to 10,000 alerts for each 24-hour period since its previous run.
* You can't [run the {{az-attack-discovery}} {{az-worker}} manually](../run-worker-on-demand.md).
