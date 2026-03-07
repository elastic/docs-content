---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Defense Evasion via Doas" prebuilt detection rule.'
---

# Potential Defense Evasion via Doas

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Defense Evasion via Doas

Doas is a command-line utility on Linux systems that allows users to execute commands as another user, typically with elevated privileges. Adversaries may exploit this by altering the Doas configuration file to gain unauthorized access or escalate privileges, bypassing security measures. The detection rule identifies suspicious activities by monitoring changes to the Doas configuration file, signaling potential misuse aimed at evading defenses.

### Possible investigation steps

- Review the alert details to confirm the file path involved is "/etc/doas.conf" and the event type is not "deletion", as specified in the query.
- Check the timestamp of the alert to determine when the configuration file was created or modified, and correlate this with any known scheduled changes or maintenance activities.
- Investigate the user account associated with the event to determine if they have legitimate reasons to modify the Doas configuration file, and verify their access permissions.
- Examine system logs and command history around the time of the alert to identify any suspicious activities or commands executed by the user.
- Assess the current Doas configuration file for unauthorized changes or entries that could indicate privilege escalation attempts.
- Cross-reference the alert with other security events or alerts from the same host to identify potential patterns or related activities that could suggest a broader attack.

### False positive analysis

- Routine administrative updates to the Doas configuration file can trigger alerts. To manage this, create exceptions for known maintenance windows or specific user accounts responsible for legitimate updates.
- Automated configuration management tools may modify the Doas configuration file as part of their normal operation. Identify these tools and exclude their activities from triggering alerts by specifying their process names or user accounts.
- System backups or restoration processes might involve creating or renaming the Doas configuration file. Exclude these processes by identifying the backup software and adding it to the exception list.
- Development or testing environments where frequent changes to the Doas configuration file are expected can generate false positives. Consider excluding these environments from monitoring or adjusting the rule to account for their unique activity patterns.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Review and revert any unauthorized changes to the Doas configuration file located at /etc/doas.conf to its last known good state.
- Conduct a thorough audit of user accounts and permissions on the affected system to identify and remove any unauthorized accounts or privilege escalations.
- Implement additional monitoring on the affected system to detect any further attempts to modify the Doas configuration file or other critical system files.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the threat has spread to other systems.
- Apply patches and updates to the affected system to address any vulnerabilities that may have been exploited by the adversary.
- Review and enhance access controls and authentication mechanisms to prevent unauthorized privilege escalation attempts in the future.
