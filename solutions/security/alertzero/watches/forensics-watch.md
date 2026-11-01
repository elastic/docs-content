---
description: "The AlertZero Forensics Watch runs forensics on attacks in Elastic Security, doing deep research on threats and exploits."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-forensics-watch}}

The {{az-forensics-watch}} does deep research on threats and exploits, running forensics on an attack.

| {{az-worker}} | What it does | Works with |
| --- | --- | --- |
| [{{az-endpoint-analysis}}](endpoint-analysis-worker.md) | Reconstructs the attack timeline on one affected host and proposes response actions. | The [{{az-attack-discovery}} {{az-worker}}](attack-discovery-worker.md) in the [{{az-triage-watch}}](triage-watch.md), which hands off the attacks this {{az-worker}} investigates. |

## When to turn on the {{az-forensics-watch}} [alertzero-forensics-watch-when]

Turn on the {{az-forensics-watch}} when you want {{alertzero}} to investigate confirmed attacks on an affected host. It works only on attacks that the [{{az-attack-discovery}} {{az-worker}}](attack-discovery-worker.md) hands off, so turn it on together with the [{{az-triage-watch}}](triage-watch.md). It also needs data from [{{elastic-defend}}](/solutions/security/configure-elastic-defend/install-elastic-defend.md) on your hosts.

% Placeholder. Above the "When to turn on" section, add a paragraph like the one on detection-watch.md: where you review its work on the Proposed Actions page, and a link to the page that explains how, with a reason to follow the link (not just "Refer to").
