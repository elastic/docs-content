---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Privilege Escalation via Windir Environment Variable" prebuilt detection rule.
---

# Privilege Escalation via Windir Environment Variable

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Privilege Escalation via Windir Environment Variable

The Windir environment variable points to the Windows directory, crucial for system operations. Adversaries may alter this variable to redirect processes to malicious directories, gaining elevated privileges. The detection rule monitors changes to this variable in the registry, flagging deviations from expected paths like "C:\windows," thus identifying potential privilege escalation attempts.

### Possible investigation steps

- Review the registry change event details to identify the specific user account associated with the altered Windir or SystemRoot environment variable. This can be done by examining the registry path and user context in the event data.
- Check the registry data strings to determine the new path set for the Windir or SystemRoot variable. Investigate if this path points to a known malicious directory or an unexpected location.
- Correlate the event with other recent registry changes or system events on the same host to identify any patterns or additional suspicious activities that might indicate a broader attack.
- Investigate the process or application that initiated the registry change by reviewing process creation logs or command-line arguments around the time of the event. This can help identify the source of the change.
- Assess the affected system for any signs of compromise or unauthorized access, such as unusual network connections, unexpected running processes, or new user accounts.
- Consult threat intelligence sources to determine if the observed behavior matches any known attack patterns or campaigns, particularly those involving privilege escalation techniques.
- If possible, restore the Windir or SystemRoot environment variable to its expected value and monitor the system for any further unauthorized changes.

### False positive analysis

- System updates or patches may temporarily alter the Windir environment variable. Monitor for these events during known maintenance windows and consider excluding them from alerts.
- Custom scripts or applications that modify environment variables for legitimate purposes can trigger false positives. Identify these scripts and whitelist their activity in the detection rule.
- User profile migrations or system restorations might change the Windir path. Exclude these operations if they are part of routine IT processes.
- Virtual environments or sandboxed applications may use different Windir paths. Verify these environments and adjust the detection rule to accommodate their specific configurations.
- Administrative tools that modify user environments for configuration management can cause alerts. Document these tools and create exceptions for their expected behavior.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Revert the Windir environment variable to its legitimate value, typically "C:\windows", to restore normal system operations.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any malicious software or scripts.
- Review recent user activity and system logs to identify any unauthorized access or changes, focusing on the time frame around the detected registry change.
- Reset passwords for any user accounts that may have been compromised, especially those with elevated privileges.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring on the affected system and similar endpoints to detect any further attempts to alter critical environment variables or other suspicious activities.
