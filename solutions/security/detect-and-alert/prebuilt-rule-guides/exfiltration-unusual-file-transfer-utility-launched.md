---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "File Transfer Utility Launched from Unusual Parent" prebuilt detection rule.
---

# File Transfer Utility Launched from Unusual Parent

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating File Transfer Utility Launched from Unusual Parent

File transfer utilities like scp, ftp, and rsync are essential for data movement in Linux environments. However, adversaries can exploit these tools to exfiltrate sensitive data. The detection rule identifies suspicious executions of these utilities by monitoring process activities, focusing on rare occurrences and unique agent IDs, which may indicate unauthorized data transfers. This helps in early detection of potential data breaches.

### Possible investigation steps

- Review the process.command_line field to understand the exact command executed and assess if it aligns with typical usage patterns or if it appears suspicious.
- Examine the process.parent.executable field to determine the parent process that initiated the file transfer utility, which may provide insights into whether the execution was part of a legitimate workflow or potentially malicious activity.
- Check the agent.id field to identify the specific host involved in the alert and correlate it with other security events or logs from the same host to gather additional context.
- Investigate the @timestamp field to verify the timing of the event and cross-reference with any known scheduled tasks or user activities that could explain the execution.
- Analyze the host.os.type field to confirm the operating system and ensure that the alert pertains to a Linux environment, as expected by the rule.

### False positive analysis

- Routine administrative tasks using file transfer utilities may trigger alerts. Regularly scheduled backups or updates using scp, rsync, or ftp should be documented and excluded from alerts by creating exceptions for known scripts or cron jobs.
- Automated system updates or patches that utilize these utilities can be mistaken for suspicious activity. Identify and whitelist the processes and command lines associated with these updates to prevent false positives.
- Internal data transfers between trusted servers for legitimate business purposes might be flagged. Establish a list of trusted agent IDs and exclude them from the rule to avoid unnecessary alerts.
- Development and testing environments often use these utilities for transferring test data. Ensure that these environments are recognized and excluded by specifying their hostnames or IP addresses in the rule configuration.
- User-initiated file transfers for legitimate reasons, such as data analysis or reporting, can be misinterpreted. Educate users to notify the security team of such activities in advance, allowing for temporary exceptions to be made.

### Response and remediation

- Immediately isolate the affected Linux system from the network to prevent further data exfiltration and unauthorized access.
- Terminate any suspicious file transfer processes identified by the alert, such as scp, ftp, or rsync, to halt ongoing data transfers.
- Conduct a thorough review of the process command lines and parent executables to identify any malicious scripts or unauthorized software that initiated the file transfer.
- Change credentials and access keys associated with the compromised system to prevent further unauthorized access.
- Escalate the incident to the security operations team for a deeper forensic analysis to determine the extent of the breach and identify any additional compromised systems.
- Implement network monitoring to detect any further attempts of unauthorized file transfers or suspicious activities from the affected system.
- Update and enhance endpoint detection and response (EDR) solutions to improve detection capabilities for similar threats in the future.

