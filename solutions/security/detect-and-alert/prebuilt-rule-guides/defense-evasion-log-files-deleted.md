---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "System Log File Deletion" prebuilt detection rule.'
---

# System Log File Deletion

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating System Log File Deletion

System logs are crucial for monitoring and auditing activities on Linux systems, providing insights into system events and user actions. Adversaries may delete these logs to cover their tracks, hindering forensic investigations. The detection rule identifies suspicious deletions of key log files, excluding benign processes like compression tools, to flag potential evasion attempts. This helps security analysts quickly respond to and investigate unauthorized log deletions.

### Possible investigation steps

- Review the specific file path involved in the deletion event to determine which log file was targeted, using the file.path field from the alert.
- Investigate the process responsible for the deletion by examining the process.name and related process metadata to identify any suspicious or unauthorized activity.
- Check for any recent login or session activity around the time of the log deletion by reviewing other logs or authentication records, focusing on the /var/log/auth.log and /var/log/secure files if they are still available.
- Analyze the user account associated with the deletion event to determine if it has a history of suspicious activity or if it was potentially compromised.
- Correlate the deletion event with other security alerts or anomalies in the system to identify any patterns or related incidents that might indicate a broader attack or compromise.
- Assess the impact of the log deletion on the system's security posture and determine if any critical forensic evidence has been lost, considering the importance of the deleted log file.

### False positive analysis

- Compression tools like gzip may trigger false positives when they temporarily delete log files during compression. To mitigate this, ensure gzip is included in the exclusion list within the detection rule.
- Automated system maintenance scripts might delete or rotate log files as part of routine operations. Review these scripts and add their process names to the exclusion list if they are verified as non-threatening.
- Docker-related processes, such as dockerd, can also cause false positives when managing container logs. Confirm these activities are legitimate and include dockerd in the exclusion list to prevent unnecessary alerts.
- Custom backup or log management tools may delete logs as part of their normal function. Identify these tools and add their process names to the exclusion list after verifying their benign nature.
- Scheduled tasks or cron jobs that manage log files should be reviewed. If they are confirmed to be safe, their associated process names should be added to the exclusion list to avoid false positives.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data tampering.
- Conduct a thorough review of user accounts and permissions on the affected system to identify any unauthorized access or privilege escalation.
- Restore deleted log files from backups if available, to aid in further forensic analysis and to maintain system integrity.
- Implement enhanced monitoring on the affected system and similar systems to detect any further unauthorized log deletions or suspicious activities.
- Escalate the incident to the security operations center (SOC) or incident response team for a comprehensive investigation and to determine the scope of the breach.
- Review and update security policies and configurations to ensure that only authorized processes can delete critical log files, leveraging access controls and audit policies.
- Consider deploying additional endpoint detection and response (EDR) solutions to improve visibility and detection capabilities for similar threats in the future.
