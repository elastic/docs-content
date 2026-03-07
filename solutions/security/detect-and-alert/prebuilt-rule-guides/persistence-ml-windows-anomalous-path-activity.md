---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Windows Path Activity" prebuilt detection rule.
---

# Unusual Windows Path Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Windows Path Activity

In corporate Windows environments, software is typically managed centrally, making execution from user or temporary directories uncommon. Adversaries exploit this by running malware from these atypical paths, bypassing standard security measures. The 'Unusual Windows Path Activity' detection rule leverages machine learning to identify such anomalies, flagging potential persistence or execution tactics used by attackers.

### Possible investigation steps

- Review the process name and path to determine if it is a known legitimate application or a suspicious executable.
- Check the parent process to understand how the process was initiated and if it correlates with expected user behavior or known software installations.
- Investigate the user account associated with the process execution to verify if the activity aligns with their typical usage patterns or if it appears anomalous.
- Examine the file hash of the executable to see if it matches known malware signatures or if it has been flagged by any threat intelligence sources.
- Look into recent file modifications or creations in the directory from which the process was executed to identify any additional suspicious files or scripts.
- Analyze network connections initiated by the process to detect any unusual or unauthorized external communications.

### False positive analysis

- Software updates or installations by IT staff can trigger alerts when executed from temporary directories. To manage this, create exceptions for known IT processes or scripts that are regularly used for legitimate software deployment.
- Some legitimate applications may temporarily execute components from user directories during updates or initial setup. Identify these applications and add them to an allowlist to prevent unnecessary alerts.
- Developers or power users might run scripts or applications from non-standard directories for testing purposes. Establish a policy to document and approve such activities, and configure exceptions for these known cases.
- Automated tasks or scripts that are scheduled to run from user directories can be mistaken for malicious activity. Review and document these tasks, then configure the detection rule to exclude them from triggering alerts.
- Security tools or monitoring software might execute diagnostic or remediation scripts from temporary paths. Verify these activities and add them to an exception list to avoid false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of potential malware and unauthorized access.
- Terminate any suspicious processes identified as running from atypical directories to halt malicious activity.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any malicious files.
- Review and restore any modified system processes or configurations to their original state to ensure system integrity.
- Collect and preserve relevant logs and evidence for further analysis and potential escalation to the incident response team.
- Escalate the incident to the security operations center (SOC) or incident response team if the threat persists or if there is evidence of broader compromise.
- Implement application whitelisting to prevent unauthorized execution of software from user or temporary directories in the future.
