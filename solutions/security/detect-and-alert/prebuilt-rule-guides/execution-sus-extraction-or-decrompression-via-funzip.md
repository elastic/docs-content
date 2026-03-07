---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Content Extracted or Decompressed via Funzip" prebuilt detection rule.'
---

# Suspicious Content Extracted or Decompressed via Funzip

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Content Extracted or Decompressed via Funzip

Funzip is a utility used to decompress files directly from a stream, often employed in legitimate data processing tasks. However, adversaries can exploit this by combining it with the 'tail' command to extract and execute malicious payloads stealthily. The detection rule identifies this misuse by monitoring specific command sequences and excluding benign processes, thus flagging potential threats for further investigation.

### Possible investigation steps

- Review the process details to confirm the presence of the 'tail' and 'funzip' command sequence, focusing on the specific arguments used, such as "-c", to understand the context of the command execution.
- Examine the parent process information to determine if the process was initiated by any known benign executables or scripts, specifically checking against the exclusion list like "/usr/bin/dracut" or "/sbin/dracut".
- Investigate the command line history and execution context of the parent process, especially if it involves "sh" or "sudo", to identify any suspicious patterns or unauthorized script executions.
- Check the file path and content being accessed by the 'tail' command to ensure it is not targeting sensitive or unexpected files, excluding known benign paths like "/var/log/messages".
- Correlate the event with other security alerts or logs from the same host to identify any related suspicious activities or patterns that might indicate a broader compromise.
- Assess the risk and impact by determining if the decompressed content was executed or if it led to any subsequent suspicious processes or network connections.

### False positive analysis

- Legitimate system maintenance tasks may trigger this rule if they involve decompressing logs or data files using funzip. To manage this, identify and exclude specific maintenance scripts or processes that are known to use funzip in a non-threatening manner.
- Automated backup or data processing operations might use funzip in combination with tail for legitimate purposes. Review these operations and add exceptions for known benign processes or scripts that match this pattern.
- Security tools or monitoring solutions like Nessus may inadvertently trigger this rule if they use similar command sequences for scanning or data collection. Exclude these tools by adding exceptions for their specific command lines or parent processes.
- Custom scripts developed in-house for data analysis or processing might use funzip and tail together. Document these scripts and exclude them from the rule to prevent false positives, ensuring they are reviewed and approved by security teams.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further spread of the potential malware.
- Terminate any suspicious processes identified by the detection rule, specifically those involving the 'tail' and 'funzip' command sequence.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malicious payloads.
- Review and analyze system logs and command history to identify any unauthorized access or additional malicious activities that may have occurred.
- Restore any compromised files or systems from known good backups to ensure integrity and availability of data.
- Implement application whitelisting to prevent unauthorized execution of utilities like 'funzip' and 'tail' by non-administrative users.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the need for broader organizational response measures.
