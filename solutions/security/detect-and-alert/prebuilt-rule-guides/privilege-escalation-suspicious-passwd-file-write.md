---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Passwd File Event Action" prebuilt detection rule.
---

# Suspicious Passwd File Event Action

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Passwd File Event Action

In Linux environments, the `/etc/passwd` file is crucial for managing user accounts. Adversaries may exploit vulnerabilities or misconfigurations to add unauthorized entries, potentially gaining root access. The detection rule monitors for the use of `openssl` to generate password entries and subsequent unauthorized modifications to the `/etc/passwd` file, flagging potential privilege escalation attempts.

### Possible investigation steps

- Review the process execution details to confirm the use of 'openssl' with the 'passwd' argument by a non-root user (user.id != "0"). This can help identify the user attempting to generate a password entry.
- Examine the process tree to understand the parent process of the 'openssl' command and determine if it was initiated by a legitimate or suspicious process.
- Check the file modification event on '/etc/passwd' to verify if the file was altered by a non-root user (user.id != "0") and ensure the process.parent.pid is not 1, indicating it wasn't initiated by the init process.
- Investigate the context of the file write event by reviewing recent logs and system changes to identify any unauthorized modifications or anomalies in user account management.
- Correlate the event with other security alerts or logs to determine if there are additional indicators of compromise or related suspicious activities on the host.

### False positive analysis

- System administrators or automated scripts may use openssl to manage user passwords without malicious intent. To handle this, identify and whitelist known administrative scripts or processes that perform legitimate password management tasks.
- Some legitimate software installations or updates might temporarily modify the /etc/passwd file. Monitor and document these activities to distinguish them from unauthorized changes, and consider creating exceptions for known software processes.
- Developers or testers might use openssl for password generation in non-production environments. Establish a policy to differentiate between production and non-production systems, and apply the rule more strictly in production environments.
- Scheduled maintenance tasks might involve legitimate modifications to the /etc/passwd file. Coordinate with IT teams to schedule these tasks and temporarily adjust monitoring rules during these periods to prevent false positives.
- In environments with multiple administrators, ensure that all legitimate administrative actions are logged and reviewed. Implement a process for administrators to report their activities, allowing for the creation of exceptions for known, non-threatening actions.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or privilege escalation attempts.
- Terminate any suspicious processes related to `openssl` or unauthorized modifications to the `/etc/passwd` file to halt ongoing malicious activities.
- Conduct a thorough review of the `/etc/passwd` file to identify and remove any unauthorized entries, especially those with root privileges.
- Reset passwords for all user accounts on the affected system to ensure no compromised credentials are used for further attacks.
- Restore the `/etc/passwd` file from a known good backup if unauthorized changes are detected and cannot be manually rectified.
- Escalate the incident to the security operations team for a comprehensive investigation into potential system vulnerabilities or misconfigurations that allowed the attack.
- Implement enhanced monitoring and alerting for similar activities, focusing on unauthorized use of `openssl` and modifications to critical system files like `/etc/passwd`.
