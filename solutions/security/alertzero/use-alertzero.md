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

{{az-workers}} do the analysis, and you decide what they bring you, such as which alerts to close, how to contain an attack, and which detection rules to change. When an {{az-investigation}} needs more than a decision, you can hand it to a teammate or escalate it.

Check a {{az-worker}}'s reasoning before you decide on what it proposes. You can't change a decision after you make it, and an approved {{az-proposed-action}} runs under your account. Each {{az-proposed-action}} appears as a card on the **{{az-proposed-actions-cap}}** page, which opens when you select **{{alertzero}}** in the navigation menu. Select a card to see the {{az-investigation}} behind it: the evidence the {{az-worker}} gathered and what it concluded.

## Where to start [alertzero-use-start]

| Your goal | Start here |
| --- | --- |
| Clear false positives out of your open alerts | [Close false-positive alerts](decide-proposed-action.md) |
| Take an attack from verdict to containment | [Respond to an attack](respond-to-attack.md) |
| Act on what a threat hunt found | [Act on a {{az-hunt-finding}}](act-on-hunt-finding.md) |
| Review proposed rule changes and new rules | [Decide a detection change](decide-detection-change.md) |
| Ask follow-up questions about the evidence | Select **Open in chat** on the card |
| Focus on one host, user, or service | Select it under **Impact** |
| Hand off an {{az-investigation}} or coordinate a response | Assign it from its card, or [Escalate an {{az-investigation}}](escalate-investigation.md) → [Track {{az-escalations}}](track-escalations.md) |
| Dismiss an {{az-investigation}} and all its pending {{az-proposed-actions}} | Close the {{az-investigation}} from its card |
| Audit recent decisions, including ones {{az-workers}} made on their own | Expand **Closed Actions**, which lists the last 72 hours. **Auto** marks the ones a {{az-worker}} approved without a person. |
