---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Privilege Escalation via Python cap_setuid" prebuilt detection rule.
---

# Potential Privilege Escalation via Python cap_setuid

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Privilege Escalation via Python cap_setuid

In Unix-like systems, setuid and setgid allow processes to execute with elevated privileges, often exploited by adversaries to gain unauthorized root access. Attackers may use Python scripts to invoke system commands with these capabilities, followed by changing user or group IDs to root. The detection rule identifies this sequence by monitoring Python processes executing system commands with setuid/setgid, followed by a root user or group ID change, signaling potential privilege escalation attempts.

### Possible investigation steps

- Review the process details, including process.entity_id and process.args, to confirm the execution of a Python script with setuid or setgid capabilities.
- Check the user.id and group.id fields to verify if there was an unauthorized change to root (user.id == "0" or group.id == "0").
- Investigate the host.id to determine if other suspicious activities or alerts have been associated with the same host.
- Examine the timeline of events to see if the uid_change or gid_change occurred immediately after the Python process execution, indicating a potential privilege escalation attempt.
- Look into the source of the Python script or command executed to identify if it was a known or unknown script, and assess its legitimacy.
- Analyze any related network activity or connections from the host around the time of the alert to identify potential lateral movement or data exfiltration attempts.

### False positive analysis

- Development and testing environments may trigger this rule when developers use Python scripts to test setuid or setgid functionalities. To manage this, exclude specific user accounts or host IDs associated with development activities.
- Automated scripts or maintenance tasks that require temporary privilege escalation might be flagged. Identify and whitelist these scripts by their process names or paths to prevent false positives.
- System administrators using Python scripts for legitimate administrative tasks could inadvertently trigger the rule. Consider excluding known administrator accounts or specific scripts used for routine maintenance.
- Security tools or monitoring solutions that simulate attacks for testing purposes may cause alerts. Exclude these tools by their process signatures or host IDs to avoid unnecessary alerts.
- Custom applications that use Python for legitimate privilege management should be reviewed and, if safe, added to an exception list based on their unique process identifiers or execution paths.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious Python processes identified by the detection rule to halt potential privilege escalation activities.
- Review and revoke any unauthorized setuid or setgid permissions on binaries or scripts to prevent exploitation.
- Conduct a thorough investigation of the affected system to identify any additional signs of compromise or persistence mechanisms.
- Reset credentials and review access permissions for any accounts that may have been affected or used in the attack.
- Apply security patches and updates to the operating system and installed software to mitigate known vulnerabilities.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems are affected.
