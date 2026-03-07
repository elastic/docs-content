---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Process Created with a Duplicated Token" prebuilt detection rule.'
---

# Process Created with a Duplicated Token

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Process Created with a Duplicated Token

In Windows environments, tokens are used to represent user credentials and permissions. Adversaries may duplicate tokens to create processes with elevated privileges, bypassing security controls. The detection rule identifies suspicious process creation by examining token usage patterns, process origins, and recent file modifications, while excluding known legitimate behaviors, to flag potential privilege escalation attempts.

### Possible investigation steps

- Review the process name and executable path to determine if it matches any known legitimate applications or if it is potentially malicious. Pay special attention to processes like powershell.exe, cmd.exe, and rundll32.exe.
- Examine the parent process and its executable path to understand the process hierarchy and identify any unusual or unexpected parent-child relationships, especially if the parent is not a typical system process.
- Check the user ID associated with the process to verify if it belongs to a legitimate user or if it appears to be an anomaly, such as a service account being used unexpectedly.
- Investigate the code signature status of the process to determine if it is trusted or if there are any issues like an expired or untrusted signature, which could indicate tampering or a malicious executable.
- Analyze the relative file creation and modification times to assess if the process was created or modified recently, which could suggest a recent compromise or unauthorized change.
- Look for any known exclusions in the query, such as specific command lines or parent processes, to ensure the alert is not a false positive based on legitimate behavior patterns.

### False positive analysis

- Processes initiated by legitimate system maintenance tools like Windows Update or system repair utilities may trigger the rule. Users can create exceptions for these processes by excluding specific parent-child process relationships that are known to be safe.
- Software installations or updates that involve temporary elevation of privileges might be flagged. Users should consider excluding processes originating from trusted directories like Program Files or Program Files (x86) if they are part of a verified installation or update process.
- Administrative scripts or automation tools that run with elevated privileges could be misidentified. Users can exclude these by specifying trusted code signatures or known script paths in the rule configuration.
- Certain legitimate applications that frequently update or modify files within a short time frame may be mistakenly flagged. Users can adjust the relative file creation or modification time thresholds or exclude specific applications by their executable paths.
- Processes that are part of normal user activity, such as those initiated by explorer.exe, may be incorrectly identified. Users can refine the rule by excluding processes with known benign parent-child relationships involving explorer.exe.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule, especially those with duplicated tokens or originating from unexpected parent processes.
- Conduct a thorough review of user accounts and privileges on the affected system to identify any unauthorized changes or escalations. Revoke any unnecessary or suspicious privileges.
- Perform a comprehensive scan of the affected system using updated antivirus and anti-malware tools to detect and remove any malicious software or scripts.
- Review recent file modifications and system logs to identify any additional indicators of compromise or unauthorized activities that may have occurred.
- Restore any altered or corrupted system files from a known good backup to ensure system integrity and functionality.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems or accounts have been compromised.
