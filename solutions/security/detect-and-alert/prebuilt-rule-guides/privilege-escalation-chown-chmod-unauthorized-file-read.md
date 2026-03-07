---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Unauthorized Access via Wildcard Injection Detected" prebuilt detection rule.
---

# Potential Unauthorized Access via Wildcard Injection Detected

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Unauthorized Access via Wildcard Injection Detected

In Linux environments, commands like `chown` and `chmod` are used to change file ownership and permissions. Adversaries may exploit wildcard characters in these commands to escalate privileges or access sensitive data by executing unintended operations. The detection rule identifies suspicious use of these commands with recursive flags and wildcard references, signaling potential misuse aimed at privilege escalation or unauthorized data access.

### Possible investigation steps

- Review the process execution details to confirm the presence of the "chown" or "chmod" command with the "-R" flag and wildcard usage in the arguments, as indicated by the query fields process.name, process.args, and event.action.
- Examine the user account associated with the process execution to determine if it has the necessary permissions to perform such operations and assess if the account has been compromised.
- Check the command execution history and related logs to identify any preceding or subsequent suspicious activities that might indicate a broader attack pattern or unauthorized access attempts.
- Investigate the source and destination of the command execution by analyzing network logs and connections to determine if the activity originated from a known or unknown IP address or host.
- Correlate this event with other alerts or anomalies in the system to identify potential patterns or coordinated attacks, focusing on privilege escalation or credential access attempts as suggested by the rule's tags and threat information.

### False positive analysis

- Routine administrative tasks using chown or chmod with recursive flags may trigger the rule. To manage this, identify and whitelist specific scripts or users that regularly perform these tasks without security risks.
- Automated system maintenance processes that involve changing file permissions or ownership across directories can be mistaken for malicious activity. Exclude these processes by specifying their command patterns or associated user accounts in the monitoring system.
- Backup operations that involve copying and setting permissions on large sets of files might be flagged. To prevent this, configure exceptions for known backup tools or scripts that use these commands in a controlled manner.
- Development environments where developers frequently change file permissions for testing purposes can generate false positives. Implement user-based exceptions for development teams to reduce unnecessary alerts.
- System updates or package installations that modify file permissions as part of their normal operation may be detected. Create exceptions for trusted package managers or update processes to avoid false alarms.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified as running the `chown` or `chmod` commands with wildcard injections to halt potential privilege escalation activities.
- Conduct a thorough review of system logs and command histories to identify any unauthorized changes made to file permissions or ownership and revert them to their original state.
- Reset credentials and review access permissions for users on the affected system to ensure no unauthorized access persists.
- Implement file integrity monitoring to detect unauthorized changes to critical files and directories in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Update and patch the affected system to address any vulnerabilities that may have been exploited during the attack, ensuring all security updates are applied.
