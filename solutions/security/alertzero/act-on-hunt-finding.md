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

The {{az-continuous-threat-hunt}} {{az-worker}} in the {{az-hunt-watch}} searches your data for activity that matches recent {{az-threat-reports}}. When the {{az-worker}} confirms a match, it adds a {{az-hunt-finding}} to the {{az-threat-report}}'s {{az-investigation}} and proposes response actions for the hosts and processes involved. The {{az-worker}} offers only {{az-manual}} {{az-autonomy}}, so every action it proposes waits for you.

To learn what the {{az-worker}} searches and which sources it draws on, refer to [](watches-and-workers.md#alertzero-hunt-watch).

## How the {{az-continuous-threat-hunt}} {{az-worker}} reports a hunt [alertzero-hunt-finding-outcomes]

Each {{az-threat-report}} has one {{az-investigation}} in each space, named after the report. The result of the hunt decides what happens to that {{az-investigation}}:

- **No confirmed match:** The {{az-worker}} closes the {{az-investigation}} as benign without asking you.
- **Confirmed match:** The {{az-investigation}} stays open with the {{az-hunt-finding}} and the {{az-proposed-actions}} that come from it.
- **Hunt didn't finish:** The {{az-investigation}} stays open, and a note in it explains which part of the hunt didn't run.

If a later hunt of the same {{az-threat-report}} confirms more activity, the {{az-worker}} reopens the {{az-investigation}} and adds the new {{az-hunt-finding}} to it.

After every hunt, the {{az-worker}} passes the attack techniques it searched for to the {{az-rule-coverage}} {{az-worker}} in the {{az-detection-watch}}, which proposes rules for any techniques your detection rules don't cover.

## How the {{az-continuous-threat-hunt}} {{az-worker}} picks response actions [alertzero-hunt-finding-how]

The {{az-worker}} proposes response actions only for hosts that run {{elastic-defend}}. It picks one response action for each process that the hunt implicates, and decides separately whether to isolate each host.

| Response action | When the {{az-worker}} proposes it |
| --- | --- |
| Kill a process | The hunt confirms that the process used a destructive technique, such as encrypting or deleting data. Or the finding is critical and the process matched an indicator of compromise (IOC) from the {{az-threat-report}}. |
| Suspend a process | The process is running, and the rules for killing it don't apply. |
| Dump a process's memory | The {{az-worker}} proposes suspending the process, and the host supports memory dumps. A memory dump keeps evidence for analysis. |
| Isolate a host | The hunt confirms lateral movement, command and control, or data exfiltration on the host. Or the hunt finds two or more suspicious processes on the host. Or the finding is critical and the host has a suspicious process. |

The {{az-worker}} doesn't propose any action for these processes:

- A protected system process, such as `lsass.exe`. The {{az-worker}} never kills or suspends one, but might propose a memory dump.
- A process that has exited.
- A process that the hunt last saw outside the period it searched, or more than seven days before the end of that period.

If another {{az-investigation}} already has the same response action waiting for the same host, the {{az-worker}} doesn't propose it again. Instead, it adds this {{az-investigation}} to the waiting {{az-proposed-action}}, and you decide the action once, in the other {{az-investigation}}.

## Review the {{az-hunt-finding}} [alertzero-hunt-finding-review]

On the **{{az-proposed-actions-cap}}** page, response actions from a hunt belong to the {{az-investigation}} named after the {{az-threat-report}}. If containing hosts isn't your role, assign the {{az-investigation}} to an incident responder.

Before you decide any response action, check that the {{az-hunt-finding}} holds up. Along with the finding's severity and the {{az-worker}}'s confidence, check these:

- **What matched:** IOCs from the {{az-threat-report}}, such as file hashes or IP addresses, or activity that matches one of the report's attack techniques.
- **Which hosts and users are involved:** Activity that's normal on those hosts, such as an admin tool that uses the same technique, points to a false match.
- **How the evidence balances:** The evidence for the match, weighed against the evidence against it.

To dig deeper, open the matching events in Discover, or ask follow-up questions in the {{az-investigation}}'s chat. If the evidence doesn't show a real threat, decline the hunt's response actions.

## Decide each response action [alertzero-hunt-finding-actions]

For each response action, check what it does and why the {{az-worker}} picked it. Make sure the {{az-hunt-finding}} implicates the host or process it targets, and consider what stops working when you act on it. For example, isolating a server also cuts off the people and services that depend on it. Then approve or decline the action:

- **If you approve:** The action runs under your account, through {{elastic-defend}}, so you need the [privileges to run it](alertzero-privileges.md#alertzero-action-privileges). If you don't have them, or the host doesn't respond within 10 minutes, the action fails, and {{alertzero}} offers it again as a new {{az-proposed-action}} with the same deadline. The {{elastic-defend}} action might still run when the host comes back online, so check the [response actions history](/solutions/security/endpoint-response-actions/response-actions-history.md) before you approve it again.
- **If you decline:** The action doesn't run. The same happens if the {{az-proposed-action}} [expires](work-in-alertzero.md) before anyone decides.

If you isolate a host, {{alertzero}} doesn't propose releasing it later. When it's safe to reconnect the host, [release it](/solutions/security/endpoint-response-actions/isolate-host.md#release-a-host) yourself. You can't undo the other response actions.

## Follow up on the analyst recommendation [alertzero-hunt-finding-recommendation]

Some findings need work that no response action covers. For these findings, the {{az-worker}} also proposes an **Analyst recommendation**. For example, it proposes one in these cases:

- The evidence involves user accounts, services, or IOCs such as IP addresses, which acting on a host doesn't contain.
- A host in the finding doesn't run {{elastic-defend}}.
- The {{az-worker}} held back a response action, such as isolating a host that doesn't support isolation.

The recommendation explains what the response actions don't cover and why. When the {{az-worker}} has them, it also lists steps to take by hand. Do the follow-up yourself, or hand it to the person who owns it. Then approve the recommendation to record that you followed up, or decline it to record that you don't need to. Neither runs anything.

## Close the {{az-investigation}} [alertzero-hunt-finding-close]

After you decide every {{az-proposed-action}} in the {{az-investigation}}, or they expire, the {{az-worker}} closes the {{az-investigation}}. The exception is an {{az-investigation}} whose finding joined a waiting {{az-proposed-action}} in another {{az-investigation}}. To close it, select **Close investigation** on its card.

To work on the finding with other people instead, [escalate the {{az-investigation}}](escalate-investigation.md).

## Next steps [alertzero-hunt-finding-next-steps]

- [Review the rules that the {{az-rule-coverage}} {{az-worker}} proposes](decide-detection-change.md#alertzero-detection-change-coverage) for the attack techniques the hunt searched for.
- [Find other work that {{az-workers}} bring you](work-in-alertzero.md).
- [Decide the response actions for an attack](respond-to-attack.md) that the {{az-attack-discovery}} {{az-worker}} finds.
- [Run response actions by hand](/solutions/security/endpoint-response-actions.md).
