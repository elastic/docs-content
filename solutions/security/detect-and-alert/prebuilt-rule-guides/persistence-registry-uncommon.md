---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Uncommon Registry Persistence Change" prebuilt detection rule.'
---

# Uncommon Registry Persistence Change

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Uncommon Registry Persistence Change

Windows Registry is a critical system database storing configuration settings. Adversaries exploit registry keys for persistence, ensuring malicious code executes on startup or during specific events. The detection rule identifies unusual modifications to less commonly altered registry keys, which may indicate stealthy persistence attempts. It filters out benign changes by excluding known legitimate processes and paths, focusing on suspicious alterations.

### Possible investigation steps

- Review the specific registry path and value that triggered the alert to understand the context of the change and its potential impact on system behavior.
- Identify the process responsible for the registry modification by examining the process.name and process.executable fields, and determine if it is a known legitimate process or potentially malicious.
- Check the registry.data.strings field to see the new data or command being set in the registry key, and assess whether it aligns with known legitimate software or suspicious activity.
- Investigate the user account associated with the registry change by reviewing the HKEY_USERS path, if applicable, to determine if the change was made by an authorized user or an unexpected account.
- Correlate the alert with other recent events on the host, such as file modifications or network connections, to identify any additional indicators of compromise or related suspicious activity.
- Consult threat intelligence sources or databases to see if the registry path or process involved is associated with known malware or adversary techniques.

### False positive analysis

- Legitimate software installations or updates may modify registry keys for setup or configuration purposes. Users can create exceptions for known software paths like C:\Program Files\*.exe to reduce noise.
- System maintenance processes such as Windows Update might trigger changes in registry keys like SetupExecute. Exclude processes like TiWorker.exe and poqexec.exe when they match known update patterns.
- Administrative scripts or tools that automate system configurations can alter registry keys. Identify and exclude these scripts by their executable paths or process names to prevent false alerts.
- Security software, including antivirus or endpoint protection, may interact with registry keys for monitoring purposes. Exclude paths related to these tools, such as C:\ProgramData\Microsoft\Windows Defender\Platform\*\MsMpEng.exe, to avoid false positives.
- User-initiated changes through control panel settings or personalization options can affect registry keys like SCRNSAVE.EXE. Exclude common system paths like %windir%\system32\rundll32.exe user32.dll,LockWorkStation to minimize false detections.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of potential malicious activity.
- Terminate any suspicious processes identified in the alert, particularly those not matching known legitimate executables or paths.
- Restore any altered registry keys to their original state using a known good backup or by manually resetting them to default values.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or processes.
- Review and update endpoint protection policies to ensure that similar registry changes are monitored and alerted on in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Document the incident, including all actions taken, to improve future response efforts and update threat intelligence databases.
