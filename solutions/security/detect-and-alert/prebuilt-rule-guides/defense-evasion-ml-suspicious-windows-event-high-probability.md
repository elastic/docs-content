---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Machine Learning Detected a Suspicious Windows Event with a High Malicious Probability Score" prebuilt detection rule.'
---

# Machine Learning Detected a Suspicious Windows Event with a High Malicious Probability Score

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Machine Learning Detected a Suspicious Windows Event with a High Malicious Probability Score

The detection leverages a machine learning model, ProblemChild, to identify potentially malicious Windows processes by analyzing patterns and assigning a high probability score to suspicious activities. Adversaries may exploit legitimate processes to evade detection, often using techniques like masquerading. This rule flags high-risk events by focusing on processes with a high malicious probability score or those identified by a blocklist, excluding known benign activities.

### Possible investigation steps

- Review the process details flagged by the ProblemChild model, focusing on those with a prediction probability greater than 0.98 or identified by the blocklist.
- Examine the command-line arguments of the suspicious process to identify any unusual or unexpected patterns, excluding those matching known benign patterns like "*C:\\WINDOWS\\temp\\nessus_*.txt*" or "*C:\\WINDOWS\\temp\\nessus_*.tmp*".
- Check the parent process of the flagged event to determine if it is a legitimate process or if it has been potentially compromised.
- Investigate the user account associated with the process to assess if it has been involved in any other suspicious activities or if it has elevated privileges that could be exploited.
- Correlate the event with other security alerts or logs to identify any related activities or patterns that could indicate a broader attack campaign.
- Consult threat intelligence sources to determine if the process or its associated indicators are linked to known malicious activities or threat actors.

### False positive analysis

- Nessus scan files in the Windows temp directory may trigger false positives due to their temporary nature and frequent legitimate use. Users can mitigate this by adding exceptions for file paths like C:\WINDOWS\temp\nessus_*.txt and C:\WINDOWS\temp\nessus_*.tmp.
- Legitimate software updates or installations might be flagged if they mimic known malicious patterns. Users should review the process details and whitelist trusted software update processes.
- System administration tools that perform actions similar to those used in attacks could be misidentified. Users should verify the legitimacy of these tools and exclude them from the rule if they are part of regular administrative tasks.
- Custom scripts or automation tools that are not widely recognized might be flagged. Users should ensure these scripts are secure and add them to an allowlist if they are part of routine operations.
- Frequent false positives from specific processes can be managed by adjusting the threshold of the machine learning model or refining the blocklist to better distinguish between benign and malicious activities.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of potential malicious activity.
- Terminate the suspicious process identified by the ProblemChild model to halt any ongoing malicious actions.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any additional threats.
- Review and analyze the process execution history and associated files to understand the scope of the compromise and identify any persistence mechanisms.
- Restore any altered or deleted files from backups, ensuring that the backup is clean and free from malware.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for similar processes and activities to detect and respond to future attempts at masquerading or defense evasion.
