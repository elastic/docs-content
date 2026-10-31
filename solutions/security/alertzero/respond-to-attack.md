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

When the {{az-attack-discovery}} {{az-worker}} finds an attack it can't rule out, {{alertzero}} brings you the decisions that take it from verdict to containment. First, you decide whether the attack needs forensics. The {{az-endpoint-analysis}} {{az-worker}} then analyzes the affected host and proposes response actions, such as isolating the host, and you decide each one. Finally, you decide whether to close the {{az-investigation}}.

## Before you begin [alertzero-respond-before]

- You need the **{{alertzero}}** and **Agent Builder** privileges set to **Read**, and the **Proposed Actions** privilege set to **All**.
- Response actions run as you, so you also need the {{elastic-defend}} sub-feature privileges for each action: **Host Isolation** or **Process Operations**, plus **Response Actions History**. Without them, the action fails. Refer to [](alertzero-privileges.md).
- To close the {{az-investigation}} and its alerts, you need the **Alerts** privilege set to **All**.
- The {{az-endpoint-analysis}} {{az-worker}} must be on, and the affected hosts must run {{elastic-defend}}. Refer to [](/solutions/security/configure-elastic-defend/install-elastic-defend.md).
- {{context-engine}} must be on in the space (the `contextEngine:enabled` advanced setting). Without it, handing an attack to forensics fails.

## Check the verdict [alertzero-respond-verdict]

The {{az-attack-discovery}} {{az-worker}} opens an {{az-investigation}} for each candidate attack and judges whether it's real. Its verdict decides what happens next:

| Verdict | What happens |
| --- | --- |
| **False positive** | {{alertzero}} closes the {{az-investigation}} and the attack, and acknowledges the open alerts without closing them. Nothing waits for you. |
| **True positive** or **Inconclusive** | {{alertzero}} asks whether to hand the attack to forensics. Continue with [Decide whether to run forensics](#alertzero-respond-handoff). |
| **Analysis failed** | The {{az-investigation}} stays open with no {{az-proposed-actions}}. Review it by hand. |

To read the verdict and its **Rationale**, select **Open in chat** on the {{az-investigation}}'s card. The verdict's **Conclusion** also appears in the {{az-investigation}}'s details.

## Decide whether to run forensics [alertzero-respond-handoff]

1. In the **Investigate** section of the **{{az-proposed-actions-cap}}** page, select the attack's card. The {{az-proposed-action}} has the attack's name as its title.
2. Decide:
    - To have the {{az-forensics-watch}} analyze the attack and propose response actions, select **Approve**. The {{az-investigation}} and the attack stay open for the forensics report. You can't undo this handoff.
    - To close the {{az-investigation}} and the attack instead, select **Decline**.

Either way, the attack's detection alerts stay open. If nobody decides within 72 hours, the {{az-proposed-action}} expires and the {{az-investigation}} stays open.

## Review the forensics report [alertzero-respond-forensics]

The {{az-endpoint-analysis}} {{az-worker}} picks up the handoff within about a minute. It analyzes one host per attack. That's the host the attack names, or else the host that appears most often in its alerts. It searches the host's {{elastic-defend}} data from around the time of the attack.

When it finishes, the {{az-investigation}}'s details show its report in the **What's happened** section:

- **Forensic timeline:** The attack's events on the host, in order, up to 50 events.
- **IOCs:** The indicators of compromise it found, such as file hashes, IP addresses, file paths, command lines, and affected identities.

If the host has no {{elastic-defend}} data from the time of the attack, {{az-endpoint-analysis}} doesn't run. Close the {{az-investigation}} by hand.

## Decide each response action [alertzero-respond-actions]

{{az-endpoint-analysis}} proposes up to eight response actions. They appear in the **Respond** section of the **{{az-proposed-actions-cap}}** page.

| Response action | Can you undo it? |
| --- | --- |
| Isolate a host | Yes, but {{alertzero}} doesn't propose releasing the host. To release it, refer to [Release a host](/solutions/security/endpoint-response-actions/isolate-host.md#release-a-host). |
| Kill a process | No. |
| Suspend a process | No. |

To decide a response action, select it and check its title, which names the host or process. Then select **Approve** or **Decline**.

An approved action runs as you, through {{elastic-defend}}. If the host doesn't respond within 10 minutes, the action fails, and {{alertzero}} can offer it again as a new {{az-proposed-action}}.

## Close the {{az-investigation}} [alertzero-respond-close]

After you decide every response action, or immediately if there are none, {{az-endpoint-analysis}} proposes closing the {{az-investigation}}. This {{az-proposed-action}} always waits for you.

- **Approve** closes the {{az-investigation}}, the attack, and its alerts. Alerts that another open attack also includes stay open.
- **Decline** keeps everything open. {{alertzero}} asks again after you decide the next {{az-proposed-action}} in the {{az-investigation}}.

To work on the attack with other people instead, select **Open an escalation** or **Attach to an escalation** from the {{az-investigation}}'s actions menu. Refer to [](escalate-investigation.md).

## How {{az-autonomy}} changes this flow [alertzero-respond-autonomy]

Both {{az-workers}} offer {{az-manual}} and {{az-supervised}} {{az-autonomy}}:

| {{az-worker}} | At {{az-manual}} | At {{az-supervised}} |
| --- | --- | --- |
| {{az-attack-discovery}} | Each handoff to forensics waits for you. | It hands off every attack it doesn't rule out, without asking. |
| {{az-endpoint-analysis}} | Each response action waits for you. | It runs its response actions without asking, as its service account. |

At either level, closing the {{az-investigation}} waits for you. To change {{az-autonomy}} levels, refer to [](configure-worker-settings.md).

## Related pages [alertzero-respond-related]

- [](decide-proposed-action.md): The steps every decision shares, and what each status means.
- [](/solutions/security/endpoint-response-actions.md): Run response actions by hand.
- [](/solutions/security/ai/attack-discovery/index.md): How Attack Discovery finds attacks.
