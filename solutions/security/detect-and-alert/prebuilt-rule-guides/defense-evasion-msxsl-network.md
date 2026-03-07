---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Network Connection via MsXsl" prebuilt detection rule.
---

# Network Connection via MsXsl

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Network Connection via MsXsl

MsXsl.exe is a legitimate Windows utility used to transform XML data using XSLT stylesheets. Adversaries exploit it to execute malicious scripts, bypassing security measures. The detection rule identifies suspicious network activity by MsXsl.exe, focusing on connections to non-local IPs, which may indicate unauthorized data exfiltration or command-and-control communication.

### Possible investigation steps

- Review the process execution details for msxsl.exe, focusing on the process.entity_id and event.type fields to confirm the process start event and gather initial context.
- Analyze the network connection details, particularly the destination.ip field, to identify the external IP address msxsl.exe attempted to connect to and assess its reputation or any known associations with malicious activity.
- Check for any related alerts or logs involving the same process.entity_id to determine if msxsl.exe has been involved in other suspicious activities or if there are patterns of behavior indicating a broader attack.
- Investigate the parent process of msxsl.exe to understand how it was launched and whether it was initiated by a legitimate application or a potentially malicious script.
- Examine the system for any additional indicators of compromise, such as unusual file modifications or other processes making unexpected network connections, to assess the scope of potential adversarial activity.

### False positive analysis

- Legitimate use of msxsl.exe for XML transformations in enterprise applications may trigger alerts. Users should identify and whitelist known applications or processes that use msxsl.exe for legitimate purposes.
- Automated scripts or scheduled tasks that utilize msxsl.exe for data processing can cause false positives. Review and document these tasks, then create exceptions for their network activity.
- Development or testing environments where msxsl.exe is used for debugging or testing XML transformations might be flagged. Ensure these environments are recognized and excluded from monitoring if they are verified as non-threatening.
- Internal network tools or monitoring solutions that leverage msxsl.exe for legitimate network communications should be identified. Add these tools to an exception list to prevent unnecessary alerts.
- Regularly review and update the list of excluded IP addresses to ensure that only trusted and verified internal IPs are exempt from triggering the rule.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized data exfiltration or command-and-control communication.
- Terminate the msxsl.exe process if it is still running to stop any ongoing malicious activity.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any malicious scripts or files associated with msxsl.exe.
- Review and analyze the network logs to identify any other systems that may have been targeted or compromised by similar activity.
- Restore the affected system from a known good backup if any critical system files or configurations have been altered.
- Implement network segmentation to limit the ability of msxsl.exe or similar utilities to make unauthorized external connections in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems or data have been impacted.
