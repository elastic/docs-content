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

# Work in {{alertzero}} [alertzero-use]

{{az-workers}} do the analysis, and you decide what they bring you, such as which alerts to close, how to contain an attack, and which detection rules to change. When the {{az-investigation}} behind a decision needs more work, you can hand it to a teammate or escalate it.

## Find the work that fits your role [alertzero-use-start]

| Your goal | Start here |
| --- | --- |
| Clear false positives out of your open alerts | [Close false-positive alerts](decide-proposed-action.md) |
| Take an attack from verdict to containment | [Respond to an attack](respond-to-attack.md) |
| Act on what a threat hunt found | [Act on a {{az-hunt-finding}}](act-on-hunt-finding.md) |
| Review proposed rule changes and new rules | [Tune noisy rules and fill detection gaps](decide-detection-change.md) |
| Ask follow-up questions about the evidence | Select **Open in chat** on the card |
| Focus on one host, user, or service | Select it in **Impacted entities** |
| Hand off the {{az-investigation}} or coordinate a response | Assign it from its card, or [escalate it](escalate-investigation.md) |
| Dismiss the {{az-investigation}} and all its pending {{az-proposed-actions}} | Close the {{az-investigation}} from its card |
| Audit recent decisions, including ones {{az-workers}} made on their own | Expand **Closed Actions**, which lists decisions from the last 72 hours. **Auto** marks the ones that {{az-workers}} approved without a person. |

% For docs writers: elastic/docs-content#9184 replaces track-escalations.md with manage-escalations.md. After it merges, add "and then [manage the {{az-escalation}}](manage-escalations.md)" to the end of the escalation row.
