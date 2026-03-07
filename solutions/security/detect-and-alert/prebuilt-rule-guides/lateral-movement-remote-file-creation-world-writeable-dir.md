---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Remote File Creation in World Writeable Directory" prebuilt detection rule.'
---

# Remote File Creation in World Writeable Directory

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Remote File Creation in World Writeable Directory

In Linux environments, world-writeable directories like `/tmp` and `/var/tmp` are used for temporary file storage, accessible by all users. Adversaries exploit these directories to deposit malicious files via remote services such as SSH or FTP, facilitating lateral movement. The detection rule identifies file creation events in these directories by non-root users using common file transfer services, signaling potential unauthorized activity.

### Possible investigation steps

- Review the file creation event details, focusing on the file path to determine if it matches any known malicious patterns or if it is unusual for the environment.
- Identify the user associated with the file creation event by examining the user.id field, and verify if this user should have access to the affected directory.
- Investigate the process responsible for the file creation by analyzing the process.name field to determine if it aligns with expected usage patterns for the user and system.
- Check the source IP address and connection details related to the file transfer service used (e.g., SSH, FTP) to identify any suspicious or unauthorized access attempts.
- Correlate the event with other recent activities on the host to identify any patterns of lateral movement or other suspicious behavior.
- Review historical data for similar file creation events by the same user or process to assess if this is part of a recurring pattern or an isolated incident.

### False positive analysis

- Routine administrative tasks: System administrators often use file transfer services like scp or rsync to move files for legitimate purposes. To reduce false positives, create exceptions for known administrative accounts or specific file paths that are regularly used for maintenance.
- Automated scripts and cron jobs: Automated processes may create temporary files in world-writeable directories. Identify and whitelist these scripts or jobs by their process names or user accounts to prevent unnecessary alerts.
- Software updates and installations: Some software updates or installations may temporarily use world-writeable directories. Monitor and document these activities, and consider excluding specific update processes or package managers from the rule.
- Development and testing environments: Developers may use these directories for testing purposes. Establish a separate monitoring policy for development environments or exclude known developer accounts to minimize false positives.
- Backup operations: Backup tools might use temporary directories for staging files. Identify these tools and their typical behavior, and create exceptions based on their process names or user IDs.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further lateral movement by the adversary.
- Terminate any suspicious processes associated with file transfer services (e.g., scp, ssh, ftp) that are not part of legitimate user activity.
- Remove any unauthorized files created in world-writeable directories such as /tmp, /var/tmp, or /dev/shm to eliminate potential threats.
- Conduct a thorough review of user accounts and permissions, focusing on non-root users who have recently accessed the system, to identify any unauthorized access.
- Reset credentials for compromised or potentially compromised accounts to prevent further unauthorized access.
- Monitor network traffic for unusual patterns or connections to external IP addresses that may indicate ongoing or additional compromise attempts.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems have been affected, ensuring a coordinated response.
