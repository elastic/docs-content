---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Base64 Encoding/Decoding Activity" prebuilt detection rule.
---

# Unusual Base64 Encoding/Decoding Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Base64 Encoding/Decoding Activity
Base64 encoding is a method to convert binary data into ASCII text, often used for data transmission. Adversaries exploit this to obfuscate malicious payloads or commands, bypassing security controls. The detection rule identifies suspicious Base64 activity on Linux by monitoring specific processes and command patterns, flagging anomalies for further investigation.

### Possible investigation steps

- Review the process name and command line arguments to understand the context of the Base64 activity. Check if the process name matches known legitimate applications or scripts.
- Examine the timestamp of the event to determine if the activity occurred during normal operational hours or if it coincides with other suspicious activities.
- Investigate the host operating system type and agent ID to identify the specific Linux system involved and assess if it has a history of similar alerts or other security incidents.
- Analyze the process command line for any unusual patterns or parameters that might indicate obfuscation or malicious intent, such as the presence of decode flags or unexpected Base64 operations.
- Correlate the event with other logs or alerts from the same host or network to identify potential lateral movement or coordinated attacks.
- Check for any recent changes or deployments on the affected system that might explain the Base64 activity, such as new software installations or updates.
- Consult threat intelligence sources to determine if the observed Base64 patterns or command line arguments are associated with known malware or attack techniques.

### False positive analysis

- Routine administrative scripts may use base64 encoding for legitimate data processing tasks. Review the process.command_line and process.args fields to identify known scripts and consider excluding them from the rule.
- Backup or data transfer operations might employ base64 encoding to handle binary data. Verify the process.name and process.command_line to ensure these operations are recognized and add exceptions for these specific processes.
- Development environments often use base64 encoding for testing purposes. Identify development-related processes by examining the process.name and process.command_line and exclude them if they are part of regular development activities.
- Automated system monitoring tools might trigger this rule if they use base64 encoding for log or data analysis. Check the agent.id and process.command_line to confirm these tools and exclude them from the rule if they are verified as non-threatening.
- Security tools that perform data encoding for analysis or reporting could be flagged. Validate these tools by reviewing the process.name and process.command_line and create exceptions for them if they are part of the security infrastructure.

### Response and remediation

- Isolate the affected Linux system from the network to prevent further data exfiltration or lateral movement by the adversary.
- Terminate any suspicious processes identified by the alert, particularly those involving base64 encoding/decoding, to halt potential malicious activity.
- Conduct a thorough review of the process command lines and arguments flagged by the alert to identify any malicious scripts or payloads. Remove or quarantine these files as necessary.
- Check for any unauthorized user accounts or privilege escalations that may have been established during the attack and revoke access immediately.
- Restore any affected systems or files from a known good backup to ensure the integrity of the system and data.
- Implement additional monitoring on the affected system and similar environments to detect any recurrence of the suspicious base64 activity.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if broader organizational impacts exist.

