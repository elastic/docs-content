---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "File with Right-to-Left Override Character (RTLO) Created/Executed" prebuilt detection rule.
---

# File with Right-to-Left Override Character (RTLO) Created/Executed

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating File with Right-to-Left Override Character (RTLO) Created/Executed

The RTLO character reverses text direction, often used to disguise file extensions, making malicious files appear benign. Adversaries exploit this to trick users into executing harmful files. The detection rule identifies suspicious file or process activities on Windows systems by scanning for RTLO characters in file paths or process names, helping to uncover potential masquerading attempts.

### Possible investigation steps

- Review the alert details to identify the specific file path or process name containing the RTLO character by examining the file.path or process.name fields.
- Check the event.type field to determine whether the alert was triggered by a file creation or process start event, which can help prioritize the investigation focus.
- Investigate the origin of the file or process by examining the file's creation time, user account involved, and any associated network activity to identify potential sources or delivery methods.
- Analyze the file or process for malicious behavior by using endpoint detection tools or sandbox environments to execute and monitor its actions.
- Cross-reference the file or process with threat intelligence databases to check for known malicious indicators or similar attack patterns.
- Review system logs and other security alerts around the same timeframe to identify any additional suspicious activities or related incidents.

### False positive analysis

- Legitimate software installations or updates may use RTLO characters in file names to manage versioning or localization, which can trigger false positives. Users can create exceptions for known software vendors or specific installation directories to reduce these alerts.
- Some file management or backup applications might use RTLO characters in temporary file names for internal processing. Identifying these applications and excluding their specific file paths from monitoring can help minimize false positives.
- Custom scripts or tools developed in-house might inadvertently use RTLO characters for legitimate purposes. Reviewing these scripts and excluding their execution paths or file names from the detection rule can prevent unnecessary alerts.
- Certain international or multilingual applications may use RTLO characters as part of their normal operation. Users should identify these applications and configure exceptions based on their file paths or process names to avoid false positives.
- In environments where file names are dynamically generated and may include RTLO characters, consider implementing a whitelist of trusted file paths or process names to reduce the likelihood of false alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further spread or communication with potential command and control servers.
- Terminate any suspicious processes identified with the RTLO character in their names to halt any ongoing malicious activity.
- Quarantine the files containing the RTLO character to prevent execution and further analysis.
- Conduct a thorough scan of the isolated system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or remnants.
- Review and analyze system logs and security alerts to determine the extent of the compromise and identify any lateral movement or additional affected systems.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional containment measures are necessary.
- Implement enhanced monitoring and detection rules to identify future attempts to use RTLO characters for masquerading, ensuring that similar threats are detected promptly.
