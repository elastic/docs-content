---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Multi-Base64 Decoding Attempt from Suspicious Location" prebuilt detection rule.
---

# Multi-Base64 Decoding Attempt from Suspicious Location

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Multi-Base64 Decoding Attempt from Suspicious Location

Base64 encoding is a common method to encode binary data into ASCII text, often used for data transmission. Adversaries exploit this by encoding malicious payloads to evade detection. The detection rule identifies suspicious decoding activities, especially from unusual directories, by monitoring rapid sequences of decoding commands. It excludes benign processes to reduce false positives, focusing on potential threats in Linux environments.

### Possible investigation steps

- Review the process details, including the parent entity ID and executable path, to understand the context of the decoding activity and identify the parent process responsible for initiating the base64 commands.
- Examine the working directory where the decoding occurred, focusing on suspicious locations such as "/tmp/*", "/var/tmp*", "/dev/shm/*", "/var/www/*", "/home/*", and "/root/*" to determine if the activity aligns with typical usage patterns or if it indicates potential malicious behavior.
- Analyze the command-line arguments used in the decoding process, specifically looking for "-d*" or "--d*" flags, to assess whether the decoding was intended to obfuscate data or execute hidden payloads.
- Investigate the sequence of events within the 3-second maxspan to identify any rapid or automated decoding attempts that could suggest scripted or malicious activity.
- Check for any exclusions in the rule, such as known benign processes or directories, to ensure the alert is not a false positive and the activity is genuinely suspicious.
- Correlate the alert with other security events or logs from the same host or network segment to gather additional context and determine if this is part of a larger attack or isolated incident.

### False positive analysis

- Scheduled tasks or cron jobs may trigger base64 decoding in benign processes. Exclude known executables like "/etc/cron.daily/vivaldi" and "/etc/cron.daily/opera-browser" to reduce false positives.
- System management tools or agents, such as those located in "/opt/microsoft/omsagent/plugin" or "/opt/rapid7/ir_agent/*", might use base64 decoding for legitimate purposes. Add these directories to the exclusion list to prevent unnecessary alerts.
- Temporary directories like "/tmp/newroot/*" may be used by legitimate applications for transient data processing. Consider excluding these paths if they are frequently involved in non-malicious activities.
- User scripts or applications in home directories may use base64 for encoding or decoding data. Monitor and whitelist specific user processes that are known to be safe to avoid false positives.
- Regularly review and update the exclusion list based on observed benign activities to ensure the rule remains effective without generating excessive false alerts.

### Response and remediation

- Immediately isolate the affected system to prevent further execution of potentially malicious payloads. Disconnect the system from the network to contain the threat.

- Review and terminate any suspicious processes identified by the detection rule, particularly those involving base64 decoding from unusual directories. Use process management tools to kill these processes.

- Conduct a thorough examination of the directories flagged by the alert (e.g., /tmp, /var/tmp, /dev/shm) to identify and remove any malicious files or scripts. Ensure these directories are cleaned of unauthorized or suspicious content.

- Restore the system from a known good backup if any malicious activity is confirmed, ensuring that the backup is free from compromise.

- Escalate the incident to the security operations team for further investigation and analysis. Provide them with logs and details of the processes and directories involved for deeper threat assessment.

- Implement additional monitoring and alerting for similar suspicious activities, focusing on rapid sequences of base64 decoding commands and unusual directory usage to enhance detection capabilities.

- Review and update access controls and permissions for the directories involved to prevent unauthorized access and execution of potentially harmful scripts or binaries.

