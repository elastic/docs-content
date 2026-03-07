---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Creation of Hidden Shared Object File" prebuilt detection rule.
---

# Creation of Hidden Shared Object File

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Creation of Hidden Shared Object File

Shared object files (.so) are dynamic libraries used in Linux environments to provide reusable code. Adversaries may exploit the ability to hide files by prefixing them with a dot, concealing malicious .so files for persistence and evasion. The detection rule identifies the creation of such hidden files, excluding benign processes like Docker, to flag potential threats.

### Possible investigation steps

- Review the alert details to identify the specific hidden shared object file (.so) that was created, noting its full path and filename.
- Investigate the process that created the file by examining the process name and its parent process, excluding "dockerd" as per the query, to determine if the process is legitimate or potentially malicious.
- Check the file creation timestamp and correlate it with other system activities or logs to identify any suspicious behavior or patterns around the time of creation.
- Analyze the contents of the hidden .so file, if accessible, to determine its purpose and whether it contains any malicious code or indicators of compromise.
- Investigate the user account associated with the file creation event to assess if the account has been compromised or is involved in unauthorized activities.
- Search for any other hidden files or suspicious activities on the system that may indicate a broader compromise or persistence mechanism.

### False positive analysis

- Development and testing environments may frequently create hidden .so files as part of routine operations. Users can mitigate this by excluding specific directories or processes known to be part of development workflows.
- Backup or system maintenance scripts might generate hidden .so files temporarily. Identify and exclude these scripts or their associated processes to prevent false alerts.
- Some legitimate software installations or updates may create hidden .so files as part of their setup process. Users should monitor installation logs and whitelist these processes if they are verified as non-threatening.
- Custom applications or services that use hidden .so files for legitimate purposes should be documented, and their creation processes should be excluded from detection to avoid unnecessary alerts.

### Response and remediation

- Isolate the affected system from the network to prevent further spread or communication with potential command and control servers.
- Terminate any suspicious processes associated with the creation of the hidden .so file, except for known benign processes like Docker.
- Remove the hidden .so file from the system to eliminate the immediate threat. Ensure that the file is securely deleted to prevent recovery.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or artifacts.
- Review system logs and process execution history to identify any unauthorized access or changes made around the time of the file creation. This can help in understanding the scope of the compromise.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and alerting for similar activities, such as the creation of hidden files, to improve detection and response times for future incidents.
