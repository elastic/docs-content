---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Data Splitting Detected" prebuilt detection rule.
---

# Potential Data Splitting Detected

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Data Splitting Detected

Data splitting utilities on Linux, such as `dd` and `split`, are typically used for managing large files by dividing them into smaller, more manageable parts. Adversaries exploit these tools to covertly exfiltrate data by splitting it into inconspicuous segments. The detection rule identifies suspicious use of these utilities by monitoring specific command-line arguments and excluding benign processes, thereby flagging potential exfiltration activities.

### Possible investigation steps

- Review the process details to confirm the use of data splitting utilities like 'dd', 'split', or 'rsplit' with suspicious arguments such as 'bs=*', 'if=*', '-b', or '--bytes*'.
- Examine the parent process name to ensure it is not a benign process like 'apport' or 'overlayroot', which are excluded in the rule.
- Investigate the source and destination paths specified in the process arguments to determine if they involve sensitive or unusual locations, excluding paths like '/tmp/nvim*', '/boot/*', or '/dev/urandom'.
- Check the user account associated with the process to assess if it has a history of legitimate use of these utilities or if it might be compromised.
- Analyze recent network activity from the host to identify any potential data exfiltration attempts, especially if the process involves external connections.
- Correlate this alert with other security events or logs from the same host to identify any patterns or additional indicators of compromise.

### False positive analysis

- Processes related to system maintenance or updates, such as those initiated by the 'apport' or 'overlayroot' processes, may trigger false positives. Users can mitigate this by ensuring these parent processes are included in the exclusion list.
- Backup operations that use 'dd' or 'split' for legitimate data management tasks can be mistaken for exfiltration attempts. Exclude specific backup scripts or processes by adding their unique identifiers or arguments to the exclusion criteria.
- Development or testing environments where 'dd' or 'split' are used for creating test data or simulating data transfer can generate false alerts. Identify and exclude these environments by specifying their process names or argument patterns.
- Automated scripts that use 'dd' or 'split' for routine data processing tasks should be reviewed and, if benign, added to the exclusion list to prevent unnecessary alerts.
- Regular system operations involving '/dev/random', '/dev/urandom', or similar sources should be excluded, as these are common in non-malicious contexts and are already partially covered by the rule's exclusions.

### Response and remediation

- Immediately isolate the affected Linux system from the network to prevent further data exfiltration.
- Terminate any suspicious processes identified by the detection rule, specifically those involving the `dd`, `split`, or `rsplit` utilities with the flagged arguments.
- Conduct a thorough review of recent file access and modification logs to identify any unauthorized data handling or exfiltration attempts.
- Restore any potentially compromised data from secure backups, ensuring that the restored data is free from any malicious alterations.
- Implement stricter access controls and monitoring on sensitive data directories to prevent unauthorized access and manipulation.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if additional systems are affected.
- Enhance monitoring and alerting for similar suspicious activities by integrating additional threat intelligence sources and refining detection capabilities.
