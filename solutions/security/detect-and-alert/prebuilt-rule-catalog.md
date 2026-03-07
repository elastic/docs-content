---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Browse all Elastic prebuilt detection rules organized by MITRE ATT&CK tactic.
---

# Prebuilt rule catalog

Browse Elastic's full library of prebuilt detection rules, organized by [MITRE ATT&CK](https://attack.mitre.org) tactic. Each rule includes the detection technique, rule type, severity, and a link to the full rule source on GitHub.

Use this catalog to:

- **Assess coverage**: See which tactics and techniques have prebuilt detection rules available.
- **Find rules by threat**: Jump to a specific tactic to find rules matching your threat model.
- **Understand rule types**: Identify which rule engine (EQL, {{esql}}, threshold, ML, and others) each rule uses, and link out to the [rule source](https://github.com/elastic/detection-rules) for full query logic, investigation notes, and false positive guidance.

To install these rules in your environment, refer to [Install prebuilt rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md). To understand the MITRE ATT&CK coverage your installed rules provide, refer to [MITRE ATT&CK coverage](/solutions/security/detect-and-alert/mitre-attack-coverage.md).

:::{note}
This catalog is automatically generated from the [elastic/detection-rules](https://github.com/elastic/detection-rules) repository. Rules are updated regularly; check the source repository for the latest changes.
:::

## Initial Access

Rules detecting techniques adversaries use to gain a first foothold in your environment, such as phishing, exploiting public-facing applications, and abusing valid accounts.

:::{csv-include} prebuilt-rule-catalog/initial-access.csv
:::

## Execution

Rules detecting techniques adversaries use to run malicious code, including command-line interpreters, scripting, and exploitation of native OS utilities.

:::{csv-include} prebuilt-rule-catalog/execution.csv
:::

## Persistence

Rules detecting techniques adversaries use to maintain access across restarts and credential changes, such as scheduled tasks, startup items, and registry modifications.

:::{csv-include} prebuilt-rule-catalog/persistence.csv
:::

## Privilege Escalation

Rules detecting techniques adversaries use to gain higher-level permissions, including exploitation of system vulnerabilities, access token manipulation, and elevation mechanism abuse.

:::{csv-include} prebuilt-rule-catalog/privilege-escalation.csv
:::

## Defense Evasion

Rules detecting techniques adversaries use to avoid detection, including disabling security tools, obfuscating code, tampering with logs, and abusing trusted processes.

:::{csv-include} prebuilt-rule-catalog/defense-evasion.csv
:::

## Credential Access

Rules detecting techniques adversaries use to steal credentials, such as dumping passwords, keylogging, brute forcing, and Kerberos attacks.

:::{csv-include} prebuilt-rule-catalog/credential-access.csv
:::

## Discovery

Rules detecting techniques adversaries use to learn about your environment, including network scanning, system enumeration, and account discovery.

:::{csv-include} prebuilt-rule-catalog/discovery.csv
:::

## Lateral Movement

Rules detecting techniques adversaries use to move through your environment, including remote services, pass-the-hash, and internal spearphishing.

:::{csv-include} prebuilt-rule-catalog/lateral-movement.csv
:::

## Collection

Rules detecting techniques adversaries use to gather data of interest before exfiltration, including screen captures, clipboard data, and email collection.

:::{csv-include} prebuilt-rule-catalog/collection.csv
:::

## Command and Control

Rules detecting techniques adversaries use to communicate with compromised systems, including web protocols, DNS tunneling, and encrypted channels.

:::{csv-include} prebuilt-rule-catalog/command-and-control.csv
:::

## Exfiltration

Rules detecting techniques adversaries use to steal data from your environment, including transfers over alternative protocols, scheduled transfers, and data compression.

:::{csv-include} prebuilt-rule-catalog/exfiltration.csv
:::

## Impact

Rules detecting techniques adversaries use to disrupt availability or compromise integrity, including data destruction, ransomware, and resource hijacking.

:::{csv-include} prebuilt-rule-catalog/impact.csv
:::

## Reconnaissance

Rules detecting techniques adversaries use to gather information for planning an attack, including active scanning and search open databases.

:::{csv-include} prebuilt-rule-catalog/reconnaissance.csv
:::

## Resource Development

Rules detecting techniques adversaries use to establish resources for operations, including acquiring infrastructure and developing capabilities.

:::{csv-include} prebuilt-rule-catalog/resource-development.csv
:::

## Other

Rules not mapped to a specific MITRE ATT&CK tactic.

:::{csv-include} prebuilt-rule-catalog/other.csv
:::
