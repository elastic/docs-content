---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Interactive Shell Launched from System User" prebuilt detection rule.'
---

# Unusual Interactive Shell Launched from System User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Interactive Shell Launched from System User

In Linux environments, system users are typically non-interactive and serve specific system functions. Adversaries may exploit these accounts to launch interactive shells, bypassing security measures and evading detection. The detection rule identifies such anomalies by monitoring process activities linked to system users, excluding legitimate processes, and flagging unexpected interactive shell launches, thus highlighting potential malicious activity.

### Possible investigation steps

- Review the process details to identify the specific interactive shell that was launched, focusing on the process.interactive:true field.
- Examine the user.name field to determine which system user account was used to launch the shell and assess whether this account should have interactive shell access.
- Investigate the process.parent.executable and process.parent.name fields to understand the parent process that initiated the shell, checking for any unusual or unauthorized parent processes.
- Analyze the process.args field for any suspicious or unexpected command-line arguments that might indicate malicious intent.
- Cross-reference the event.timestamp with other security logs to identify any correlated activities or anomalies around the same time frame.
- Check for any recent changes or anomalies in the system user's account settings or permissions that could have facilitated the shell launch.
- Assess the risk and impact of the activity by considering the context of the system and the potential for further malicious actions.

### False positive analysis

- System maintenance tasks may trigger interactive shells from system users like 'daemon' or 'systemd-timesync'. To handle these, review the specific maintenance scripts and add exceptions for known benign processes.
- Automated backup or update processes might launch interactive shells under system users such as 'backup' or 'apt'. Identify these processes and exclude them by adding their parent process names or arguments to the exception list.
- Some monitoring or logging tools may use system accounts like 'messagebus' or 'dbus' to execute interactive shells. Verify these tools and exclude their activities if they are legitimate and necessary for system operations.
- Custom scripts or applications running under system users for specific tasks could be misidentified. Document these scripts and add their process names to the exclusion criteria to prevent false alerts.
- In environments where certain system users are repurposed for non-standard tasks, ensure these tasks are documented and create exceptions for their associated processes to avoid unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious interactive shell sessions initiated by system users to halt potential malicious activities.
- Conduct a thorough review of the affected system's logs and processes to identify any additional indicators of compromise or unauthorized changes.
- Reset credentials for the compromised system user accounts and any other accounts that may have been accessed or affected.
- Implement stricter access controls and monitoring for system user accounts to prevent unauthorized interactive shell launches in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Update detection mechanisms and rules to enhance monitoring for similar threats, ensuring that any future attempts are quickly identified and addressed.
