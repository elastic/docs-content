---
navigation_title: Remap to MITRE ATT&CK v19
applies_to:
  stack: ga 9.5
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Learn what changed in MITRE ATT&CK v19 and how to find and remap custom detection rules affected by the update.
---

# Remap detection rules to MITRE ATT&CK v19 [remap-mitre-attack]

[MITRE ATT&CK](https://attack.mitre.org) v19 retires the Defense Evasion tactic and replaces it with two new tactics: Stealth and Defense Impairment. This page helps you understand how to find custom rules affected by the change and remap them so your coverage stays accurate.

::::{note}
When you create or edit a custom rule, the tactic and technique options in **Advanced settings** only include MITRE ATT&CK v19. You can't map a rule to a tactic or technique from v18 or earlier.
::::

## Before you begin [remap-mitre-attack-before-you-begin]

To remap custom rules, you need privileges to manage rules. Refer to [Detections privileges](/solutions/security/detect-and-alert/detections-privileges.md#detections-privileges-manage-rules) for details.

## What changed in v19 [remap-mitre-attack-what-changed]

The core change in v19 is the Defense Evasion tactic split. It reorganizes how the Impair Defenses ([T1562](https://attack.mitre.org/techniques/T1562/)) technique is structured, and v19 also adds a handful of new techniques.

### Defense Evasion tactic split [remap-mitre-attack-defense-evasion-split]

MITRE retired the Defense Evasion tactic ([TA0005](https://attack.mitre.org/tactics/TA0005/)) and replaced it with two tactics, split by adversary intent:

| Tactic | ID | Intent | Example techniques |
| :---- | :---- | :---- | :---- |
| **Stealth** | [TA0005](https://attack.mitre.org/tactics/TA0005/) (reuses the retired ID) | Avoid detection | Hide artifacts, obfuscation, masquerading |
| **Defense Impairment** | [TA0112](https://attack.mitre.org/tactics/TA0112/) | Disable or break defenses | Disable EDR, modify firewall rules, modify cloud compute configuration |

Most former Defense Evasion techniques moved into Stealth or Defense Impairment. A smaller number moved to Execution, Lateral Movement, or Privilege Escalation instead.

### Impair Defenses (T1562) restructuring [remap-mitre-attack-impair-defenses]

As part of the split, [T1562](https://attack.mitre.org/techniques/T1562/) (Impair Defenses), [T1562.001](https://attack.mitre.org/techniques/T1562/001/), and [T1562.006](https://attack.mitre.org/techniques/T1562/006/) were merged into a new parent technique, [T1685 (Disable or Modify Tools)](https://attack.mitre.org/techniques/T1685/). The remaining T1562 sub-techniques were revoked and reissued under new IDs in Defense Impairment.

Review any rule, exception, or dashboard that references T1562 or its sub-techniques.

### New techniques [remap-mitre-attack-new-techniques]

Beyond the tactic split, v19 also introduces techniques that didn't exist in earlier versions. You don't need to remap anything for these, but you can map new or existing custom rules to them going forward.

| Technique | Tactic |
| :---- | :---- |
| Disable or Modify System Firewall: Windows Host Firewall ([T1686.003](https://attack.mitre.org/techniques/T1686/003/)) | Defense Impairment |
| Exploitation for Defense Impairment ([T1687](https://attack.mitre.org/techniques/T1687/)) | Defense Impairment |
| Social Engineering ([T1684](https://attack.mitre.org/techniques/T1684/)) | Stealth |


## Find rules that need remapping [remap-mitre-attack-find-rules]

A rule is flagged if it's mapped to the Defense Evasion tactic under its pre-v19 definition, to [T1562](https://attack.mitre.org/techniques/T1562/) or a sub-technique merged into [T1685](https://attack.mitre.org/techniques/T1685/), or to any other technique or sub-technique revoked in v19. 

To find rules that need to be remapped, check the following places:

* A callout on the **{{siem-rules-ui}}** page, titled **MITRE ATT&CK updated to v19**, links to the coverage page and notes that affected rules are flagged there and on each rule's edit form.
* A callout on the **MITRE ATT&CK coverage** page shows how many rules are affected. Select **View rules** to see the affected rules, each with the specific outdated tactic, technique, or sub-technique ID it references.
* On an individual rule's details page, any outdated ID is marked with a warning icon next to it in the **MITRE ATT&CK** field. Hover over the icon to see which ID is affected.

## Remap your rules [remap-mitre-attack-remap-rules]

If you only use Elastic prebuilt rules, mappings are updated for you automatically. If you have custom rules mapped to MITRE ATT&CK, remap them manually:

:::::{stepper}
::::{step} Review flagged rules
Go to the **MITRE ATT&CK coverage** page and select **View rules** in the outdated mappings callout to see the affected rules and the specific ID each one references. Select a rule to open its details page, where the outdated mapping is marked with a warning icon, then select **Edit rule**.

In the rule editor, flagged mappings appear outlined in red under **MITRE ATT&CK threats** in **Advanced settings**, with an inline error naming the outdated ID.

:::{note}
Prebuilt rules that aren't installed, and custom rules that are unmapped or mapped to a deprecated tactic or technique, don't appear on the coverage grid.
:::
::::

::::{step} Remap T1562 references first
Point rules mapped to [T1562](https://attack.mitre.org/techniques/T1562/), [T1562.001](https://attack.mitre.org/techniques/T1562/001/), or [T1562.006](https://attack.mitre.org/techniques/T1562/006/) to [T1685 (Disable or Modify Tools)](https://attack.mitre.org/techniques/T1685/). Remap any other revoked T1562 sub-techniques to their reissued Defense Impairment IDs.
::::

::::{step} Remap remaining Defense Evasion rules by intent
For each rule still mapped to the old Defense Evasion tactic, decide whether the underlying behavior is about evading detection (map to Stealth, [TA0005](https://attack.mitre.org/tactics/TA0005/)) or disabling a control (map to Defense Impairment, [TA0112](https://attack.mitre.org/tactics/TA0112/)). 

Some techniques might belong under Execution, Lateral Movement, or Privilege Escalation instead. Review the linked MITRE ATT&CK pages to compare technique descriptions before you decide.
::::

::::{step} (Optional) Update custom saved searches and dashboards
Update any custom saved search, dashboard, or report that filters or groups by TA0005 under its old meaning, and add equivalent views for TA0112.

:::{dropdown} How to find and update these references
Each alert stores its own copy of its rule's MITRE mapping, in the `kibana.alert.rule.threat.tactic.id` and `kibana.alert.rule.threat.tactic.name` fields. Remapping a rule only affects new alerts, so a saved search or dashboard filtering on `TA0005` can match both older Defense Evasion alerts and newer Stealth alerts. 

To update affected saved searches and dashboards:  

1. **Locate the reference** - Open a saved search, dashboard panel, or report you know filters or breaks down by tactic. Look at its KQL query or filter pills (for example, `kibana.alert.rule.threat.tactic.id : "TA0005"` or `kibana.alert.rule.threat.tactic.name : "Defense Evasion"`). For a Lens or TSVB panel, the field used in a **Group by** or **Break down by** aggregation.
2. **Decide the new value** - After you remap the rule, `TA0005` means Stealth going forward, but alerts generated before the remap keep their original Defense Evasion meaning under that same ID. To cover both old Defense Evasion alerts and new Defense Impairment alerts in one view, filter on both `TA0005` and `TA0112`—for example, `kibana.alert.rule.threat.tactic.id : ("TA0005" or "TA0112")`. If you only want current Stealth alerts going forward, leave it as `TA0005` alone.
3. **Save your changes** - Edit the filter or query directly in the saved search or dashboard panel, then save it.
:::
::::

::::{step} Verify on the coverage page
Filter to enabled rules and confirm the Stealth and Defense Impairment columns match your expected coverage, and that the list of rules with outdated mappings contains no rules (or only the rules you intend to leave mapped to a previous MITRE ATT&CK version).
::::
:::::

## Related [remap-mitre-attack-related]

* [MITRE ATT&CK coverage](/solutions/security/detect-and-alert/mitre-attack-coverage.md)
* [MITRE ATT&CK v19 release notes](https://attack.mitre.org/resources/updates/updates-april-2026/)
