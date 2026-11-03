---
description: "Review a hunt finding from the AlertZero Continuous Threat Hunt Worker in Elastic Security, decide the response actions it proposes, and follow up on what a response action can't handle."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Act on a {{az-hunt-finding}} [alertzero-act-on-hunt-finding]

The {{az-continuous-threat-hunt}} {{az-worker}} in the {{az-hunt-watch}} searches your data for activity that matches recent {{az-threat-reports}}. When the {{az-continuous-threat-hunt}} {{az-worker}} confirms a match, it adds a {{az-hunt-finding}} to the {{az-threat-report}}'s {{az-investigation}} and proposes response actions for the hosts and processes involved.

The {{az-continuous-threat-hunt}} {{az-worker}} offers only {{az-manual}} {{az-autonomy}}, so every action it proposes waits for a person. To learn what the {{az-worker}} searches and which sources it draws on, refer to [](watches-and-workers.md).

% For docs writers: After the Watches and Workers reference (elastic/docs-content-internal#1814) merges, link to its Hunt Watch section instead of the whole page.

## How the {{az-continuous-threat-hunt}} {{az-worker}} reports a hunt [alertzero-hunt-finding-outcomes]

Each {{az-threat-report}} has one {{az-investigation}} in each space, named after the report. The result of the hunt decides what happens to that {{az-investigation}}:

- **No confirmed match:** The {{az-continuous-threat-hunt}} {{az-worker}} closes the {{az-investigation}} as benign without asking you.
- **Confirmed match:** The {{az-investigation}} stays open with the {{az-hunt-finding}} and the {{az-proposed-actions}} that come from it.
- **Hunt didn't finish:** The {{az-investigation}} stays open, and a note in the {{az-investigation}} explains which part of the hunt didn't run.

If a later hunt of the same {{az-threat-report}} confirms more activity, the {{az-continuous-threat-hunt}} {{az-worker}} reopens the {{az-investigation}} and adds the new {{az-hunt-finding}} to it.

## Check the evidence in the {{az-hunt-finding}} [alertzero-hunt-finding-check]

Before you decide any response action, make sure the evidence shows a real threat in your environment.

1. In the **Respond** section of the **{{az-proposed-actions-cap}}** page, select a response action from the hunt. Its title names the action and the host, such as `Isolate host WIN-ANALYST01`. The {{az-investigation}} opens in a flyout.
2. Find the **{{az-hunt-finding-cap}}**. It names the {{az-threat-report}} it came from and shows the finding's severity and the {{az-continuous-threat-hunt}} {{az-worker}}'s confidence as a percentage.
3. Check that the evidence holds:
    - **Hunt result:** **Confirmed by** shows how the hunt confirmed the match. **IOC Hunt** means your events contain indicators of compromise (IOCs) from the {{az-threat-report}}, such as file hashes or IP addresses. **Behavior Hunt** means your events show activity that matches an attack technique from the report.
    - **Affected hosts** and **Affected users:** Look for activity that's normal on those hosts, such as an admin tool that uses the same technique. Normal activity points to a false match.
    - **Evidence for** and **Evidence against:** Weigh what supports the match against what argues against it.

    To see the matching events, select **Open events in Discover**. To ask follow-up questions about the evidence, select **Open chat**.

If the evidence doesn't show a real threat, decline the response actions from the hunt.

## How the {{az-continuous-threat-hunt}} {{az-worker}} picks response actions [alertzero-hunt-finding-how]

The {{az-continuous-threat-hunt}} {{az-worker}} proposes response actions only for hosts that run {{elastic-defend}}. For each process that the hunt implicates, the {{az-worker}} picks one response. For each host, the {{az-worker}} decides separately whether to isolate it.

| Response action | When the {{az-continuous-threat-hunt}} {{az-worker}} proposes it |
| --- | --- |
| Kill a process | The hunt confirms that the process used a destructive technique, such as encrypting or deleting data. Or the finding is critical and the process matched an indicator from the {{az-threat-report}}. |
| Suspend a process | The process is running, and the rules for killing it don't apply. |
| Dump a process's memory | The {{az-worker}} proposes suspending the process, and the host supports memory dumps. A memory dump keeps evidence for analysis. Memory dumps appear in the **Investigate** section. |
| Isolate a host | The hunt confirms lateral movement, command and control, or data exfiltration on the host. Or the hunt finds two or more suspicious processes on the host. Or the finding is critical and the host has a suspicious process. |

The {{az-continuous-threat-hunt}} {{az-worker}} doesn't propose any action for these processes:

- A protected system process, such as `lsass.exe`. The {{az-worker}} never kills or suspends one, but might propose a memory dump.
- A process that has exited.
- A process that the hunt last saw outside the period it searched, or more than seven days before the end of that period.

If another {{az-investigation}} already has the same response action waiting for the same host, the {{az-continuous-threat-hunt}} {{az-worker}} doesn't propose the action again. Instead, the {{az-worker}} adds this {{az-investigation}} to the waiting {{az-proposed-action}}, and you decide the action once, in the other {{az-investigation}}.

## Decide each response action [alertzero-hunt-finding-actions]

If containing hosts isn't your role, assign the {{az-investigation}} to an incident responder from its card. To decide a response action:

1. Select the response action.
2. Check **Action** and **Why**. The **Why** list starts with the rule that picked the action. Make sure the {{az-hunt-finding}} implicates the host or process, and consider what stops working when you act on it. For example, isolating a server also cuts off the people and services that depend on it.
3. Select **Approve** or **Decline**.
    - **If you approve:** The action runs under your account, through {{elastic-defend}}. Approving doesn't give you the privileges to run the action. Refer to [](alertzero-privileges.md). If you don't have those privileges, or the host doesn't respond within 10 minutes, the {{az-proposed-action}} shows **Failed**. {{alertzero}} then offers the action again as a new {{az-proposed-action}} with the same deadline. The {{elastic-defend}} action might still run when the host comes back online, so check the [response actions history](/solutions/security/endpoint-response-actions/response-actions-history.md) before you approve it again.
    - **If you decline:** The action doesn't run.

    Each {{az-proposed-action}} expires 72 hours after the {{az-continuous-threat-hunt}} {{az-worker}} proposes it. If nobody decides before then, the action doesn't run.

% For docs writers: After elastic/docs-content#9158 merges, link to alertzero-privileges.md#alertzero-action-privileges.

## Undo a response action [alertzero-hunt-finding-undo]

Host isolation is the only response action you can undo. {{alertzero}} doesn't propose releasing the host, so when it's safe to reconnect it, [release the host](/solutions/security/endpoint-response-actions/isolate-host.md#release-a-host) yourself.

## Follow up on the analyst recommendation [alertzero-hunt-finding-recommendation]

Some findings need work that no response action covers. For these findings, the {{az-continuous-threat-hunt}} {{az-worker}} also adds the **Analyst recommendation** {{az-proposed-action}} in the **Respond** section. For example, the {{az-worker}} adds one in these cases:

- The evidence involves user accounts, services, or indicators such as IP addresses, which acting on a host doesn't contain.
- A host in the finding doesn't run {{elastic-defend}}.
- The {{az-continuous-threat-hunt}} {{az-worker}} held back a response action, such as isolating a host that doesn't support isolation.

To follow up:

1. Select **Analyst recommendation**.
2. Read the recommendation:
    - **Why:** What the response actions don't cover.
    - **Held back:** Response actions that the {{az-continuous-threat-hunt}} {{az-worker}} didn't propose, and why. This section appears only when the {{az-worker}} held back an action.
    - **Recommended steps:** What to do by hand. This section appears only when the {{az-worker}} has steps to suggest.
3. Do the follow-up yourself, or hand it to the person who owns it.
4. Select **Approve** to record that you followed up, or **Decline** to record that the follow-up isn't needed. Neither runs anything.

## Close the {{az-investigation}} [alertzero-hunt-finding-close]

After you decide every {{az-proposed-action}} in the {{az-investigation}}, or they expire, the {{az-continuous-threat-hunt}} {{az-worker}} closes the {{az-investigation}}.

If the finding joined the waiting {{az-proposed-action}} in another {{az-investigation}}, this {{az-investigation}} doesn't close on its own. Close it yourself from its card.

To work on the finding with other people instead, escalate the {{az-investigation}}. Refer to [](escalate-investigation.md).

## Turn what the hunt searched into detection rules [alertzero-hunt-finding-coverage]

Every hunt, including one with no confirmed match, passes the attack techniques it searched for to the {{az-rule-coverage}} {{az-worker}} in the {{az-detection-watch}}. The {{az-rule-coverage}} {{az-worker}} checks whether your detection rules cover those techniques, and proposes rules for the gaps in the **Configure** section. To review those rules, refer to [](decide-detection-change.md#alertzero-detection-change-coverage).

## Related pages [alertzero-hunt-finding-related]

- [](use-alertzero.md): Find other work that {{az-workers}} bring you.
- [](respond-to-attack.md): Decide the response actions for an attack that the {{az-attack-discovery}} {{az-worker}} finds.
- [](/solutions/security/endpoint-response-actions.md): Run response actions by hand.
