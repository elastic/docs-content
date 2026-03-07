---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "SSL Certificate Deletion" prebuilt detection rule.
---

# SSL Certificate Deletion

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating SSL Certificate Deletion
SSL certificates are crucial for establishing secure communications in Linux environments. Adversaries may delete these certificates to undermine trust and disrupt system operations, often as part of defense evasion tactics. The detection rule identifies suspicious deletions by monitoring specific directories for certificate files, excluding benign processes, thus highlighting potential malicious activity.

### Possible investigation steps

- Review the alert details to confirm the file path and extension of the deleted SSL certificate, ensuring it matches the pattern "/etc/ssl/certs/*" with extensions "pem" or "crt".
- Identify the process responsible for the deletion by examining the process name and compare it against the exclusion list (e.g., "dockerd", "pacman") to determine if the process is potentially malicious.
- Investigate the user account associated with the process that performed the deletion to assess if the account has a history of suspicious activity or unauthorized access.
- Check system logs and audit trails around the time of the deletion event to identify any related activities or anomalies that could indicate a broader attack or compromise.
- Assess the impact of the certificate deletion on system operations and security, including any disruptions to secure communications or trust relationships.
- If the deletion is deemed suspicious, consider restoring the deleted certificate from backups and implementing additional monitoring to detect further unauthorized deletions.

### False positive analysis

- Routine system updates or package installations may trigger certificate deletions. Exclude processes like package managers or update services that are known to perform these actions.
- Automated certificate renewal services might delete old certificates as part of their renewal process. Identify and exclude these services to prevent false alerts.
- Custom scripts or maintenance tasks that manage SSL certificates could be flagged. Review and whitelist these scripts if they are verified as non-malicious.
- Backup or cleanup operations that involve certificate files might cause false positives. Ensure these operations are recognized and excluded from monitoring.
- Development or testing environments where certificates are frequently added and removed can generate alerts. Consider excluding these environments if they are isolated and secure.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or damage.
- Verify the deletion of SSL certificates by checking the specified directories and confirm the absence of expected certificate files.
- Restore deleted SSL certificates from a secure backup to re-establish secure communications and trust controls.
- Conduct a thorough review of system logs and process activity to identify the source of the deletion and any associated malicious activity.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement additional monitoring on the affected system and similar environments to detect any further unauthorized deletions or related suspicious activities.
- Review and update access controls and permissions to ensure only authorized processes and users can modify or delete SSL certificates.
