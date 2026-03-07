---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "WebServer Access Logs Deleted" prebuilt detection rule.
---

# WebServer Access Logs Deleted

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating WebServer Access Logs Deleted

Web server access logs are crucial for monitoring and analyzing web traffic, providing insights into user activity and potential security incidents. Adversaries may delete these logs to cover their tracks, hindering forensic investigations. The detection rule identifies log deletions across various operating systems by monitoring specific file paths, signaling potential attempts at evasion or evidence destruction.

### Possible investigation steps

- Review the specific file path where the deletion event was detected to determine which web server's logs were affected, using the file.path field from the alert.
- Check for any recent access or modification events on the affected web server to identify potential unauthorized access or suspicious activity prior to the log deletion.
- Investigate user accounts and processes that had access to the deleted log files around the time of the deletion event to identify potential malicious actors or compromised accounts.
- Correlate the log deletion event with other security alerts or anomalies in the same timeframe to identify patterns or related incidents.
- Examine backup logs or alternative logging mechanisms, if available, to recover deleted information and assess the impact of the log deletion on forensic capabilities.

### False positive analysis

- Routine log rotation or maintenance scripts may delete old web server logs. To handle this, identify and exclude these scheduled tasks from triggering alerts by specifying their execution times or associated process names.
- Automated backup processes that move or delete logs after archiving can trigger false positives. Exclude these processes by adding exceptions for the backup software or scripts used.
- Development or testing environments where logs are frequently cleared to reset the environment can cause alerts. Consider excluding these environments by specifying their IP addresses or hostnames.
- System administrators manually deleting logs as part of regular maintenance can be mistaken for malicious activity. Implement a policy to log and approve such actions, and exclude these approved activities from detection.
- Temporary log deletions during server migrations or upgrades might trigger alerts. Document these events and create temporary exceptions during the migration period.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Conduct a thorough review of recent user activity and system changes to identify any unauthorized access or modifications that may have led to the log deletion.
- Restore the deleted web server access logs from backups, if available, to aid in further forensic analysis and investigation.
- Implement enhanced monitoring on the affected system to detect any further attempts at log deletion or other suspicious activities.
- Review and tighten access controls and permissions on log files to ensure only authorized personnel can modify or delete them.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are compromised.
- Document the incident, including all actions taken, and update incident response plans to improve future detection and response capabilities.
