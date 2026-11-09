---
description: "Take an attack that AlertZero finds in Elastic Security from its Attack Discovery verdict to containment, with a forensics report and response actions from Endpoint Analysis."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Respond to an attack [alertzero-respond-to-attack]

The {{az-attack-discovery}} {{az-worker}} opens an {{az-investigation}} for each potential attack it finds, and then judges whether the attack is real. For each attack that it confirms or can't rule out, its [{{az-autonomy}}](configure-worker-settings.md) controls what happens next:

- With **{{az-manual}}** {{az-autonomy}} (the default), the {{az-worker}} proposes sending the attack for forensics and waits for you to [approve or decline](#alertzero-respond-handoff) it.
- With **{{az-supervised}}** {{az-autonomy}}, the {{az-worker}} sends the attack for forensics on its own. You [check what ran](#alertzero-respond-autonomy) afterward.

In forensics, the {{az-endpoint-analysis}} {{az-worker}} analyzes the affected host, reports what happened on it, and proposes response actions, such as isolating the host. An incident responder usually takes over from there to decide each response action and whether to close the {{az-investigation}}.

## How the {{az-attack-discovery}} {{az-worker}} judges an attack [alertzero-respond-verdict]

The {{az-attack-discovery}} {{az-worker}} gives each attack a verdict, and the verdict decides what {{alertzero}} does:

- **True positive or inconclusive:** Depending on its {{az-autonomy}}, the {{az-worker}} proposes sending the attack for forensics or sends it on its own.
- **False positive:** {{alertzero}} closes the {{az-investigation}} and the attack without asking you, and marks the attack's open alerts as acknowledged.
- **Analysis failed:** The {{az-investigation}} stays open with no {{az-proposed-actions}}. Review the attack yourself.

## Decide whether to send the attack for forensics [alertzero-respond-handoff]

Open the attack on the **{{az-proposed-actions-cap}}** page, and check the verdict and the reasoning behind it. Then approve or decline sending the attack for forensics:

- **If you approve:** The {{az-endpoint-analysis}} {{az-worker}} analyzes the attack and proposes response actions. The {{az-investigation}} and the attack stay open for the forensics report. You can't undo this approval.
- **If you decline:** The {{az-investigation}} and the attack close. {{alertzero}} marks the attack's open alerts as acknowledged, but doesn't close them.

If the {{az-proposed-action}} [expires](work-in-alertzero.md) before anyone decides, the {{az-investigation}} stays open.

## How the {{az-endpoint-analysis}} {{az-worker}} analyzes an attack [alertzero-respond-analysis]

The {{az-endpoint-analysis}} {{az-worker}} analyzes one host per attack. It picks the host that the attack names or, if the attack names none, the host that appears most often in the attack's alerts. Then it searches that host's {{elastic-defend}} data from around the time of the attack. If the host has no {{elastic-defend}} data from that time, the {{az-worker}} doesn't run, and no report appears. Close the {{az-investigation}} yourself.

The {{az-worker}} writes what it finds into a forensics report. When the report shows malicious activity on the host, the {{az-worker}} also proposes response actions. It picks the most specific action that the evidence in the report supports:

- **Kill or suspend a process:** When the evidence identifies the process, such as by its process ID.
- **Isolate the host:** When the evidence identifies the host, but not a specific process.

If the evidence doesn't identify the host or process that an action needs, the {{az-worker}} doesn't propose that action.

## Read the forensics report [alertzero-respond-forensics]

The forensics report in the {{az-investigation}}'s details shows what the attack did on the host:

- **Forensic timeline:** The attack's events on the host, in order.
- **IOCs:** The indicators of compromise that the {{az-endpoint-analysis}} {{az-worker}} found, such as file hashes, IP addresses, file paths, command lines, and affected identities.

Because the report covers only one host, check whether its IOCs appear on your other hosts to find out which ones the attack reached.

## Decide each response action [alertzero-respond-actions]

On the **{{az-proposed-actions-cap}}** page, an attack's response actions belong to the {{az-investigation}} named after the attack. Each one explains the evidence it rests on and what it stops. Check which host or process it targets, and make sure the forensics report implicates it. Consider what stops working when you act on it. For example, isolating a server also cuts off the people and services that depend on it. Then approve or decline the action:

- **If you approve:** The action runs under your account, through {{elastic-defend}}, so you need the [privileges to run it](alertzero-privileges.md). If you don't have them, or the host doesn't respond within 10 minutes, the action fails, and {{alertzero}} offers it again as a new {{az-proposed-action}} with the same deadline. The {{elastic-defend}} action might still run when the host comes back online, so check the [response actions history](/solutions/security/endpoint-response-actions/response-actions-history.md) before you approve it again.
- **If you decline:** The action doesn't run. The same happens if the {{az-proposed-action}} [expires](work-in-alertzero.md) before anyone decides.

If you isolate a host, {{alertzero}} doesn't propose releasing it later. When it's safe to reconnect the host, [release it](/solutions/security/endpoint-response-actions/isolate-host.md#release-a-host) yourself. You can't undo the other response actions.

## Check what ran without you [alertzero-respond-autonomy]

Your team can set either {{az-worker}} to {{az-supervised}} {{az-autonomy}}, so the {{az-worker}} acts without waiting for you:

- **{{az-attack-discovery}} {{az-worker}}:** Sends attacks for forensics without asking.
- **{{az-endpoint-analysis}} {{az-worker}}:** Runs its response actions without asking.

To see which response actions ran, check **Closed Actions** on the **{{az-proposed-actions-cap}}** page for actions that the {{az-endpoint-analysis}} {{az-worker}} approved, or check the [response actions history](/solutions/security/endpoint-response-actions/response-actions-history.md). If the {{az-endpoint-analysis}} {{az-worker}} isolated a host and it's safe to reconnect the host, [release it](/solutions/security/endpoint-response-actions/isolate-host.md#release-a-host).

## Close the {{az-investigation}} [alertzero-respond-close]

When no response actions are waiting for a decision, the {{az-endpoint-analysis}} {{az-worker}} proposes closing the {{az-investigation}}. This {{az-proposed-action}} always waits for you, even when the {{az-workers}} run at {{az-supervised}} {{az-autonomy}}.

- **If you approve:** The {{az-investigation}}, the attack, and its alerts close. Alerts that another open attack also includes stay open.
- **If you decline:** Everything stays open. {{alertzero}} asks again after you decide the next {{az-proposed-action}} in the {{az-investigation}}.

To work on the attack with other people instead, [escalate the {{az-investigation}}](escalate-investigation.md).

## Next steps [alertzero-respond-next-steps]

- [Find other work that {{az-workers}} bring you](work-in-alertzero.md).
- [Run response actions by hand](/solutions/security/endpoint-response-actions.md).
- [Learn how Attack Discovery finds attacks](/solutions/security/ai/attack-discovery/index.md).
