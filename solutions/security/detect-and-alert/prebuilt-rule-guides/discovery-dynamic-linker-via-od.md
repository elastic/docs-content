---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Dynamic Linker Discovery via od" prebuilt detection rule.
---

# Suspicious Dynamic Linker Discovery via od

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Dynamic Linker Discovery via od

The dynamic linker in Linux environments is crucial for loading shared libraries needed by programs. Attackers may exploit the `od` utility to inspect these linkers, seeking vulnerabilities for code injection. The detection rule identifies suspicious use of `od` targeting specific linker files, flagging potential reconnaissance activities that could precede an exploit attempt.

### Possible investigation steps

- Review the process execution details to confirm the use of the 'od' utility, focusing on the process name and arguments to ensure they match the suspicious patterns identified in the query.
- Investigate the user account associated with the process execution to determine if the activity aligns with their typical behavior or if it appears anomalous.
- Check the system's process execution history for any other unusual or related activities around the same time, such as attempts to access or modify linker files.
- Analyze any network connections or data transfers initiated by the host around the time of the alert to identify potential data exfiltration or communication with known malicious IPs.
- Correlate this event with other security alerts or logs from the same host to identify patterns or sequences of actions that could indicate a broader attack campaign.

### False positive analysis

- System administrators or developers may use the od utility to inspect dynamic linker files for legitimate debugging or system maintenance purposes. To handle this, create exceptions for known user accounts or processes that regularly perform these activities.
- Automated scripts or monitoring tools might invoke od on dynamic linker files as part of routine system checks. Identify these scripts and whitelist their execution paths to prevent unnecessary alerts.
- Security researchers or penetration testers could use od during authorized security assessments. Establish a process to temporarily disable the rule or add exceptions for the duration of the assessment to avoid false positives.
- Some software installations or updates might involve the use of od to verify linker integrity. Monitor installation logs and correlate with od usage to determine if the activity is benign, and consider adding exceptions for these specific scenarios.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement or further exploitation.
- Terminate any suspicious processes associated with the `od` utility that are targeting dynamic linker files to halt any ongoing reconnaissance or exploitation attempts.
- Conduct a thorough review of system logs and process execution history to identify any unauthorized access or modifications to the dynamic linker files.
- Restore any altered or compromised dynamic linker files from a known good backup to ensure system integrity.
- Implement stricter access controls and monitoring on critical system files, including dynamic linkers, to prevent unauthorized access and modifications.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems are affected or if there is a broader threat campaign.
- Update detection and monitoring systems to enhance visibility and alerting for similar suspicious activities involving the `od` utility and critical system files.
