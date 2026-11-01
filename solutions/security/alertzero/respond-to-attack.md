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

When the {{az-attack-discovery}} {{az-worker}} finds an attack it can't rule out, you decide whether to send it for forensics. The {{az-endpoint-analysis}} {{az-worker}} then analyzes the affected host, reports what happened on it, and proposes response actions, such as isolating the host. You decide each response action, then whether to close the {{az-investigation}}.

## Decide whether to run forensics [alertzero-respond-handoff]

{{alertzero}} asks you about each attack that the {{az-attack-discovery}} {{az-worker}} judges a true positive or inconclusive. When the {{az-worker}} judges an attack a false positive, {{alertzero}} closes the {{az-investigation}} and the attack without asking. When the analysis fails, the {{az-investigation}} stays open with no {{az-proposed-actions}}, so review the attack yourself.

1. In the **Investigate** section of the **{{az-proposed-actions-cap}}** page, select the attack's card.
2. Check the verdict and why the {{az-attack-discovery}} {{az-worker}} reached it. To read the verdict and its **Rationale**, select **Open in chat**. The verdict's **Conclusion** also appears in the {{az-investigation}}'s details.
3. Select **Approve** or **Decline**.
    - **If you approve:** The {{az-endpoint-analysis}} {{az-worker}} analyzes the attack and proposes response actions. The {{az-investigation}} and the attack stay open for the forensics report. You can't undo this approval.
    - **If you decline:** The {{az-investigation}} and the attack close.

    Either way, the attack's detection alerts stay open. By default, the {{az-proposed-action}} expires after 72 hours. If nobody decides before then, the {{az-investigation}} stays open.

## Review the forensics report [alertzero-respond-forensics]

The forensics report shows what the attack did on the affected host. It appears in the **What's happened** section of the {{az-investigation}}'s details:

- **Forensic timeline:** The attack's events on the host, in order.
- **IOCs:** The indicators of compromise that the {{az-endpoint-analysis}} {{az-worker}} found, such as file hashes, IP addresses, file paths, command lines, and affected identities.

The {{az-endpoint-analysis}} {{az-worker}} analyzes one host per attack: The host the attack names, or else the host that appears most often in the attack's alerts. It searches that host's {{elastic-defend}} data from around the time of the attack. Because the report covers only one host, check whether its IOCs appear on your other hosts to find out which ones the attack reached.

If the host has no {{elastic-defend}} data from the time of the attack, the {{az-endpoint-analysis}} {{az-worker}} doesn't run, and no report appears. Close the {{az-investigation}} yourself.

## Decide each response action [alertzero-respond-actions]

The {{az-endpoint-analysis}} {{az-worker}} proposes response actions, such as isolating a host or killing or suspending a process. They appear in the **Respond** section of the **{{az-proposed-actions-cap}}** page.

1. Select a response action.
2. Check the host or process that the action's title names, and make sure the forensics report implicates it. Consider what stops working when you act on it. For example, isolating a server also cuts off the people and services that depend on it.
3. Select **Approve** or **Decline**.
    - **If you approve:** The action runs under your account, through {{elastic-defend}}. If the host doesn't respond within 10 minutes, the {{az-proposed-action}} shows **Failed**, and {{alertzero}} might offer it again as a new {{az-proposed-action}}. The {{elastic-defend}} action might still run when the host comes back online, so check the [response actions history](/solutions/security/endpoint-response-actions/response-actions-history.md) before you approve it again.
    - **If you decline:** The action doesn't run.

You can undo only host isolation. {{alertzero}} doesn't propose releasing an isolated host, so release it yourself when it's safe. Refer to [Release a host](/solutions/security/endpoint-response-actions/isolate-host.md#release-a-host). You can't undo killing or suspending a process.

## Close the {{az-investigation}} [alertzero-respond-close]

After you decide every response action, or right away if there are none, the {{az-endpoint-analysis}} {{az-worker}} proposes closing the {{az-investigation}}. This {{az-proposed-action}} always waits for you, so a person confirms the response is done before anything closes.

- **If you approve:** The {{az-investigation}}, the attack, and its alerts close. Alerts that another open attack also includes stay open.
- **If you decline:** Everything stays open. {{alertzero}} asks again after you decide the next {{az-proposed-action}} in the {{az-investigation}}.

To work on the attack with other people instead, escalate the {{az-investigation}}. Refer to [](escalate-investigation.md).

## Check response actions that ran on their own [alertzero-respond-autonomy]

If your team sets the {{az-endpoint-analysis}} {{az-worker}} to {{az-supervised}} {{az-autonomy}}, it runs its response actions without waiting for you. If your team sets the {{az-attack-discovery}} {{az-worker}} to {{az-supervised}}, it sends attacks for forensics without asking. Either way, the {{az-proposed-action}} to close the {{az-investigation}} still waits for you.

To see what ran, expand **Closed Actions** on the **{{az-proposed-actions-cap}}** page and look for cards marked **Auto**, or check the [response actions history](/solutions/security/endpoint-response-actions/response-actions-history.md). If the {{az-endpoint-analysis}} {{az-worker}} isolated a host and it's safe to bring the host back, release it. Refer to [Release a host](/solutions/security/endpoint-response-actions/isolate-host.md#release-a-host).

## Related pages [alertzero-respond-related]

- [](use-alertzero.md): Find other work that {{az-workers}} bring you.
- [](/solutions/security/endpoint-response-actions.md): Run response actions by hand.
- [](/solutions/security/ai/attack-discovery/index.md): How Attack Discovery finds attacks.
