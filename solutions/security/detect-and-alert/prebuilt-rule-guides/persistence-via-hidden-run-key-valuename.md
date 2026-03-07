---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Persistence via Hidden Run Key Detected" prebuilt detection rule.
---

# Persistence via Hidden Run Key Detected

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Persistence via Hidden Run Key Detected

The Windows Registry is a critical system database that stores configuration settings. Adversaries exploit it for persistence by creating hidden registry keys using native APIs, making them invisible to standard tools like regedit. The detection rule identifies changes in specific registry paths associated with startup programs, flagging null-terminated keys that suggest stealthy persistence tactics.

### Possible investigation steps

- Review the specific registry path where the change was detected to determine if it matches any of the paths listed in the query, such as "HKEY_USERS\\*\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\" or "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\".
- Check the timestamp of the registry change event to correlate it with other system activities or user actions that occurred around the same time.
- Investigate the process that made the registry change by examining process creation logs or using tools like Sysmon to identify the responsible process and its parent process.
- Analyze the content of the registry key value that was modified or created to determine if it points to a legitimate application or a potentially malicious executable.
- Cross-reference the detected registry change with known threat intelligence sources to identify if the key or value is associated with known malware or adversary techniques.
- Assess the affected system for additional indicators of compromise, such as unusual network connections, file modifications, or other persistence mechanisms.

### False positive analysis

- Legitimate software installations or updates may create registry keys in the specified paths, leading to false positives. Users can monitor the installation process and temporarily disable the rule during known software updates to prevent unnecessary alerts.
- System administrators may intentionally configure startup programs for maintenance or monitoring purposes. Document these configurations and create exceptions in the detection rule to avoid flagging them as threats.
- Some security software may use similar techniques to ensure their components start with the system. Verify the legitimacy of such software and whitelist their registry changes to prevent false alarms.
- Custom scripts or automation tools used within an organization might modify registry keys for operational reasons. Identify these scripts and exclude their activities from the detection rule to reduce false positives.
- Regularly review and update the list of known safe applications and processes that interact with the registry paths in question, ensuring that the detection rule remains relevant and accurate.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Use a trusted tool to manually inspect and remove the hidden registry keys identified in the alert from the specified registry paths to eliminate the persistence mechanism.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or processes associated with the threat.
- Review recent user activity and system logs to identify any unauthorized access or changes made by the adversary, and reset credentials for any compromised accounts.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
- Implement enhanced monitoring on the affected system and similar endpoints to detect any recurrence of the threat, focusing on registry changes and process execution.
- Update and reinforce endpoint security configurations to prevent similar persistence techniques, such as enabling registry auditing and restricting access to critical registry paths.
