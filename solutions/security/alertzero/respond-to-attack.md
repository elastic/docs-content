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

When the {{az-attack-discovery}} {{az-worker}} finds an attack it can't rule out, a triage analyst decides whether to send it for forensics. The {{az-endpoint-analysis}} {{az-worker}} then analyzes the affected host, reports what happened on it, and proposes response actions, such as isolating the host. An incident responder usually takes over from there to decide each response action and whether to close the {{az-investigation}}.

## How the {{az-attack-discovery}} {{az-worker}} sorts attacks [alertzero-respond-how]

The {{az-attack-discovery}} {{az-worker}} gives each attack a verdict, and the verdict decides what {{alertzero}} does:

- **True positive or inconclusive:** {{alertzero}} asks whether to send the attack for forensics.
- **False positive:** {{alertzero}} closes the {{az-investigation}} and the attack without asking you, and marks the attack's open alerts as acknowledged.
- **Analysis failed:** The {{az-investigation}} stays open with no {{az-proposed-actions}}. Review the attack yourself.

## Decide whether to send the attack for forensics [alertzero-respond-handoff]

1. In the **Investigate** section of the **{{az-proposed-actions-cap}}** page, select the attack's card.
2. Check the verdict and why the {{az-attack-discovery}} {{az-worker}} reached it. To read the verdict and its **Rationale**, select **Open chat**. The verdict's **Conclusion** also appears in the {{az-investigation}}'s details.
3. Select **Approve** or **Decline** for each proposed action.
    - **If you approve:** The {{az-endpoint-analysis}} {{az-worker}} analyzes the attack and proposes response actions. The {{az-investigation}} and the attack stay open for the forensics report. You can't undo this approval.
    - **If you decline:** The {{az-investigation}} and the attack close. {{alertzero}} marks the attack's open alerts as acknowledged, but doesn't close them.

    The {{az-proposed-action}} expires after 72 hours. If nobody decides before then, the {{az-investigation}} stays open.

## Read the forensics report [alertzero-respond-forensics]

The forensics report shows what the attack did on the affected host. It appears in the **What's happened** section of the {{az-investigation}}'s details:

- **Forensic timeline:** The attack's events on the host, in order.
- **IOCs:** The indicators of compromise that the {{az-endpoint-analysis}} {{az-worker}} found, such as file hashes, IP addresses, file paths, command lines, and affected identities.

The {{az-endpoint-analysis}} {{az-worker}} analyzes one host per attack. It picks the host that the attack names or, if the attack names none, the host that appears most often in the attack's alerts. Then it searches that host's {{elastic-defend}} data from around the time of the attack.

Because the report covers only one host, check whether its IOCs appear on your other hosts to find out which ones the attack reached.

If the host has no {{elastic-defend}} data from the time of the attack, the {{az-endpoint-analysis}} {{az-worker}} doesn't run, and no report appears. Close the {{az-investigation}} yourself.

## Decide each response action [alertzero-respond-actions]

The {{az-endpoint-analysis}} {{az-worker}}'s response actions appear in the **Respond** section of the **{{az-proposed-actions-cap}}** page.

1. Select a response action.
2. Check the host or process that the action's title names, and make sure the forensics report implicates it. Consider what stops working when you act on it. For example, isolating a server also cuts off the people and services that depend on it.
3. Select **Approve** or **Decline**.
    - **If you approve:** The action runs under your account, through {{elastic-defend}}. For privileges that you need to run the action, refer to [](alertzero-privileges.md). If the host doesn't respond within 10 minutes, the {{az-proposed-action}} shows **Failed**, and {{alertzero}} might offer it again as a new {{az-proposed-action}}. The {{elastic-defend}} action might still run when the host comes back online, so check the [response actions history](/solutions/security/endpoint-response-actions/response-actions-history.md) before you approve it again.
    - **If you decline:** The action doesn't run.

## Undo a response action [alertzero-respond-undo]

Host isolation is the only response action you can undo. {{alertzero}} doesn't propose releasing the host, so when it's safe to reconnect it, [release the host](/solutions/security/endpoint-response-actions/isolate-host.md#release-a-host) yourself.

## Close the {{az-investigation}} [alertzero-respond-close]

After you decide every response action, or immediately if there are none, the {{az-endpoint-analysis}} {{az-worker}} proposes closing the {{az-investigation}}. This {{az-proposed-action}} always waits for you, even when the {{az-workers}} run at {{az-supervised}} {{az-autonomy}}.

- **If you approve:** The {{az-investigation}}, the attack, and its alerts close. Alerts that another open attack also includes stay open.
- **If you decline:** Everything stays open. {{alertzero}} asks again after you decide the next {{az-proposed-action}} in the {{az-investigation}}.

To work on the attack with other people instead, escalate the {{az-investigation}}. Refer to [](escalate-investigation.md).

## Check response actions that ran without you [alertzero-respond-autonomy]

Your team can set either {{az-worker}} to {{az-supervised}} {{az-autonomy}}, so the {{az-worker}} acts without waiting for you:

- **{{az-attack-discovery}} {{az-worker}}:** Sends attacks for forensics without asking.
- **{{az-endpoint-analysis}} {{az-worker}}:** Runs its response actions without asking.

To see what ran, expand **Closed Actions** on the **{{az-proposed-actions-cap}}** page and look for cards approved by the {{az-endpoint-analysis}} {{az-worker}}, or check the [response actions history](/solutions/security/endpoint-response-actions/response-actions-history.md). If the {{az-endpoint-analysis}} {{az-worker}} isolated a host and it's safe to bring the host back, [release it](#alertzero-respond-undo).

## Related pages [alertzero-respond-related]

- [](use-alertzero.md): Find other work that {{az-workers}} bring you.
- [](/solutions/security/endpoint-response-actions.md): Run response actions by hand.
- [](/solutions/security/ai/attack-discovery/index.md): Learn how Attack Discovery finds attacks.
