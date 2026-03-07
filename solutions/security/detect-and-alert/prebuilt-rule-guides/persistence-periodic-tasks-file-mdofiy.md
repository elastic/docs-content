---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Persistence via Periodic Tasks" prebuilt detection rule.'
---

# Potential Persistence via Periodic Tasks

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Persistence via Periodic Tasks

Periodic tasks in macOS are scheduled operations that automate system maintenance and other routine activities. Adversaries may exploit these tasks to execute unauthorized code or maintain persistence by altering task configurations. The detection rule identifies suspicious file activities related to periodic task configurations, excluding deletions, to flag potential misuse. This helps in early detection of persistence mechanisms employed by attackers.

### Possible investigation steps

- Review the file path specified in the alert to determine which configuration file was created or modified. Focus on paths like /private/etc/periodic/*, /private/etc/defaults/periodic.conf, or /private/etc/periodic.conf.
- Examine the contents of the modified or newly created configuration file to identify any unauthorized or suspicious entries that could indicate malicious activity.
- Check the timestamp of the file modification or creation to correlate with any known suspicious activities or other alerts in the same timeframe.
- Investigate the user account and process responsible for the file modification to determine if it aligns with expected behavior or if it indicates potential compromise.
- Look for any related events in the system logs that might provide additional context or evidence of unauthorized access or persistence attempts.
- Assess the risk and impact of the changes by determining if the modified periodic task could execute malicious code or provide persistence for an attacker.

### False positive analysis

- Routine system updates or maintenance scripts may trigger alerts when they modify periodic task configurations. Users can create exceptions for known update processes by identifying their specific file paths or process names.
- Administrative tools or scripts used by IT departments for legitimate system management might alter periodic task settings. To mitigate this, users should whitelist these tools by verifying their source and ensuring they are part of authorized IT operations.
- Custom user scripts for personal automation tasks could be flagged if they modify periodic task configurations. Users should document and exclude these scripts by adding them to an exception list, ensuring they are reviewed and approved for legitimate use.
- Security software or monitoring tools that adjust system settings for protection purposes might inadvertently trigger the rule. Users should verify these tools' activities and exclude them if they are confirmed to be part of the security infrastructure.

### Response and remediation

- Isolate the affected macOS system from the network to prevent potential lateral movement or further execution of unauthorized code.
- Review the identified periodic task configuration files for unauthorized modifications or additions. Restore any altered files to their original state using known good backups.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any malicious code that may have been executed through the periodic tasks.
- Check for any additional persistence mechanisms that may have been established by the adversary, such as other scheduled tasks or startup items, and remove them.
- Monitor the system and network for any signs of continued unauthorized activity or attempts to re-establish persistence.
- Escalate the incident to the security operations team for further investigation and to determine if other systems may be affected.
- Implement enhanced monitoring and alerting for changes to periodic task configurations to quickly detect similar threats in the future.
