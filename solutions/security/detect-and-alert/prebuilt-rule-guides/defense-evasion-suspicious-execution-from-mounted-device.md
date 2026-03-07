---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Execution from a Mounted Device" prebuilt detection rule.
---

# Suspicious Execution from a Mounted Device

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Execution from a Mounted Device

In Windows environments, script interpreters and signed binaries are essential for executing legitimate tasks. However, adversaries can exploit these by launching them from non-standard directories, such as mounted devices, to bypass security measures. The detection rule identifies such anomalies by monitoring processes initiated from unexpected directories, especially when triggered by common parent processes like explorer.exe, thus flagging potential defense evasion attempts.

### Possible investigation steps

- Review the process details to confirm the executable path and working directory, ensuring they match the criteria of being launched from a non-standard directory (e.g., not from "C:\\").
- Investigate the parent process, explorer.exe, to determine if there are any unusual activities or user actions that might have triggered the suspicious execution.
- Check the user account associated with the process to verify if the activity aligns with their typical behavior or if the account might be compromised.
- Analyze the command line arguments used by the suspicious process to identify any potentially malicious scripts or commands being executed.
- Correlate the event with other security alerts or logs from the same host to identify any patterns or additional indicators of compromise.
- Examine the mounted device from which the process was executed to determine its origin, legitimacy, and any associated files that might be malicious.

### False positive analysis

- Legitimate software installations or updates may trigger the rule if they are executed from a mounted device. Users can create exceptions for known software update processes that are verified as safe.
- Portable applications running from USB drives or external storage can be flagged. To mitigate this, users should whitelist specific applications that are frequently used and deemed non-threatening.
- IT administrative scripts executed from network shares or mounted drives for maintenance tasks might be detected. Users can exclude these scripts by specifying trusted network paths or script names.
- Development environments where scripts are tested from non-standard directories can cause alerts. Developers should ensure their working directories are recognized as safe or use designated development machines with adjusted monitoring rules.
- Backup or recovery operations that utilize mounted devices for script execution may be misidentified. Users should identify and exclude these operations by defining exceptions for known backup tools and processes.

### Response and remediation

- Isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes identified by the detection rule, such as those initiated by script interpreters or signed binaries from non-standard directories.
- Conduct a forensic analysis of the mounted device and the affected system to identify any malicious payloads or scripts and remove them.
- Review and restore any altered system configurations or registry settings to their original state to ensure system integrity.
- Update and patch the system to close any vulnerabilities that may have been exploited by the attacker.
- Monitor for any recurrence of similar activities by enhancing logging and alerting mechanisms, focusing on process execution from non-standard directories.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
