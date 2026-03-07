---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Shadow File Read via Command Line Utilities" prebuilt detection rule.'
---

# Potential Shadow File Read via Command Line Utilities

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Shadow File Read via Command Line Utilities

In Linux environments, the `/etc/shadow` file stores hashed passwords, making it a prime target for attackers seeking credential access. Adversaries with elevated privileges may exploit command-line utilities to read this file, aiming to extract credentials for lateral movement. The detection rule identifies suspicious access attempts by monitoring process activities related to the file, excluding legitimate operations, thus highlighting potential unauthorized access attempts.

### Possible investigation steps

- Review the process details to identify the executable and arguments used, focusing on the process.args field to confirm access attempts to /etc/shadow.
- Check the process.parent.name field to determine the parent process and assess if it is associated with known legitimate activities or suspicious behavior.
- Investigate the user context under which the process was executed to verify if the user had legitimate reasons to access the /etc/shadow file.
- Examine the host's recent activity logs for any privilege escalation events that might have preceded the access attempt, indicating potential unauthorized privilege elevation.
- Correlate the event with other alerts or logs from the same host to identify patterns or sequences of actions that suggest lateral movement or further credential access attempts.
- Assess the environment for any recent changes or deployments that might explain the access attempt, such as updates or configuration changes involving user management.

### False positive analysis

- System maintenance tasks may trigger alerts when legitimate processes like chown or chmod access the /etc/shadow file. To handle these, consider excluding these specific processes when they are executed by trusted system administrators during scheduled maintenance.
- Containerized environments might generate false positives if processes within containers access the /etc/shadow file. Exclude paths such as /var/lib/docker/* or /run/containerd/* to reduce noise from container operations.
- Security tools like wazuh-modulesd or custom scripts (e.g., gen_passwd_sets) that legitimately interact with the /etc/shadow file for monitoring or compliance checks can be excluded by adding them to the process.parent.name exclusion list.
- Automated scripts or cron jobs that perform routine checks or updates on system files, including /etc/shadow, should be reviewed and, if deemed safe, excluded from triggering alerts by specifying their process names or paths in the exclusion criteria.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious processes identified in the alert that are attempting to access the /etc/shadow file.
- Conduct a thorough review of user accounts and privileges on the affected system to identify any unauthorized privilege escalations or account creations.
- Change all passwords for accounts on the affected system, especially those with elevated privileges, to mitigate the risk of credential compromise.
- Review and update access controls and permissions for sensitive files like /etc/shadow to ensure they are restricted to only necessary users and processes.
- Monitor for any further attempts to access the /etc/shadow file across the network, using enhanced logging and alerting mechanisms to detect similar threats.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems have been compromised.
