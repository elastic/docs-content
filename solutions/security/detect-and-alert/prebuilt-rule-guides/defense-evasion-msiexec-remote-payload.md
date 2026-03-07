---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Remote Install via MsiExec" prebuilt detection rule.
---

# Potential Remote Install via MsiExec

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Remote Install via MsiExec

MsiExec is a Windows utility for installing, maintaining, and removing software. Adversaries exploit it to execute malicious payloads by disguising them as legitimate installations. The detection rule identifies suspicious child processes spawned by MsiExec that initiate network activity, which is atypical for standard installations. By focusing on unusual executable paths and network connections, the rule helps uncover potential misuse indicative of malware delivery or initial access attempts.

### Possible investigation steps

- Review the process tree to identify the parent and child processes of the suspicious MsiExec activity, focusing on the process.entity_id and process.parent.name fields to understand the execution flow.
- Examine the process.executable path to determine if it deviates from typical installation paths, as specified in the query, to assess the likelihood of malicious activity.
- Analyze the network or DNS activity associated with the process by reviewing the event.category field for network or dns events, and correlate these with the process.name to identify any unusual or unauthorized connections.
- Check the process.args for any unusual or suspicious command-line arguments that might indicate an attempt to execute malicious payloads or scripts.
- Investigate the host's recent activity and security logs to identify any other indicators of compromise or related suspicious behavior, leveraging data sources like Elastic Defend, Sysmon, or SentinelOne as mentioned in the rule's tags.
- Assess the risk and impact of the detected activity by considering the context of the alert, such as the host's role in the network and any potential data exposure or system compromise.

### False positive analysis

- Legitimate software installations or updates may trigger the rule if they involve network activity. Users can create exceptions for known software update processes that are verified as safe.
- Custom enterprise applications that use MsiExec for deployment and require network access might be flagged. Identify these applications and exclude their specific executable paths from the rule.
- Automated deployment tools that utilize MsiExec and perform network operations could be misidentified. Review these tools and whitelist their processes to prevent false alerts.
- Security software or system management tools that leverage MsiExec for legitimate purposes may cause false positives. Confirm these tools' activities and add them to an exclusion list if necessary.
- Regularly review and update the exclusion list to ensure it reflects the current environment and any new legitimate software that may interact with MsiExec.

### Response and remediation

- Isolate the affected system from the network immediately to prevent further malicious activity and lateral movement.
- Terminate the suspicious child process spawned by MsiExec to halt any ongoing malicious operations.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malicious payloads or remnants.
- Review and analyze the process execution and network activity logs to identify any additional indicators of compromise (IOCs) and assess the scope of the intrusion.
- Reset credentials and review access permissions for any accounts that may have been compromised or used during the attack.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and detection rules to identify similar threats in the future, focusing on unusual MsiExec activity and network connections.
