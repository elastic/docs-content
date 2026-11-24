---
description: "Find the work that AlertZero Workers bring you in Elastic Security, see which proposed actions fit your role, and follow up on investigations and escalations."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Work in {{alertzero}} [alertzero-work]

{{az-workers}} do the analysis, and you decide what they bring you, such as which alerts to close, how to contain an attack, and which detection rules to change. When the {{az-investigation}} behind a decision needs more work, you can hand it to a teammate or escalate it.

Each kind of work waits in its own section of the **{{az-proposed-actions-cap}}** page:

- **Investigate:** Alert closures, attacks to send for forensics, and memory dumps.
- **Respond:** Response actions, analyst recommendations, and the {{az-proposed-action}} that closes an attack's {{az-investigation}}.
- **Configure:** Detection rule changes.

Each {{az-proposed-action}} expires 72 hours after a {{az-worker}} proposes it. If nobody decides before then, the action doesn't run, and the {{az-proposed-action}} shows **Expired**.

## Find the work that fits your role [alertzero-work-start]

| Your goal | Start here |
| --- | --- |
| Clear false positives out of your open alerts | [Close false-positive alerts](close-false-positive-alerts.md) |
| Take an attack from verdict to containment | [Respond to an attack](respond-to-attack.md) |
| Act on what a threat hunt found | [Act on a {{az-hunt-finding}}](act-on-hunt-finding.md) |
| Review proposed rule changes and new rules | [Tune noisy rules and fill detection gaps](decide-detection-change.md) |
| Ask follow-up questions about the evidence | Select **Open in chat** on the card |
| Focus on one host, user, or service | Select it in **Impacted entities** |
| Hand off the {{az-investigation}} or coordinate a response | Assign it from its card, or [escalate it](escalate-investigation.md) and then [manage the {{az-escalation}}](manage-escalations.md) |
| Close the {{az-investigation}} and dismiss all its pending {{az-proposed-actions}} | Select **Close investigation** on its card |
| Audit recent decisions, including ones {{az-workers}} made on their own | Expand **Closed Actions**, which lists decisions from the last 72 hours. A decision that a {{az-worker}} made on its own names the {{az-worker}} that made it. |
