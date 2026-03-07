---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Remote File Execution via MSIEXEC" prebuilt detection rule.'
---

# Potential Remote File Execution via MSIEXEC

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Remote File Execution via MSIEXEC

MSIEXEC, the Windows Installer, facilitates software installation, modification, and removal. Adversaries exploit it to execute remote MSI files, bypassing security controls. The detection rule identifies suspicious MSIEXEC activity by monitoring process starts, network connections, and child processes, filtering out known benign signatures and paths, thus highlighting potential misuse for initial access or defense evasion.

### Possible investigation steps

- Review the process start event for msiexec.exe to identify the command-line arguments used, focusing on the presence of the "/V" flag, which indicates a remote installation attempt.
- Examine the network connection attempts associated with msiexec.exe to determine the remote IP addresses or domains being contacted, and assess their reputation or any known associations with malicious activity.
- Investigate the child processes spawned by msiexec.exe, especially those not matching known benign executables or paths, to identify any suspicious or unexpected activity.
- Check the user ID associated with the msiexec.exe process to verify if it aligns with expected user behavior or if it indicates potential compromise, especially focusing on user IDs like "S-1-5-21-*" or "S-1-5-12-1-*".
- Analyze the code signature of any child processes to ensure they are trusted and expected, paying particular attention to any unsigned or untrusted executables.
- Correlate the alert with any recent phishing attempts or suspicious emails received by the user, as the MITRE ATT&CK technique T1566 (Phishing) is associated with this rule.

### False positive analysis

- Legitimate software installations using msiexec.exe may trigger the rule. To manage this, create exceptions for known software update processes that use msiexec.exe with trusted code signatures.
- System maintenance tasks that involve msiexec.exe, such as Windows updates or system repairs, can be excluded by identifying and allowing specific system paths and executables involved in these processes.
- Enterprise software deployment tools that utilize msiexec.exe for remote installations might cause false positives. Exclude these by verifying the code signature and adding exceptions for trusted deployment tools.
- Administrative scripts or automation tools that invoke msiexec.exe for legitimate purposes should be reviewed and, if verified as safe, excluded based on their execution context and code signature.
- Network monitoring tools or security software that simulate msiexec.exe activity for testing or monitoring purposes can be excluded by identifying their specific signatures and paths.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or data exfiltration. This can be done by disabling network interfaces or moving the system to a quarantine VLAN.
- Terminate the msiexec.exe process if it is still running to stop any ongoing malicious activity. Use task management tools or scripts to ensure the process is completely stopped.
- Conduct a thorough review of the system for any unauthorized changes or installations. Check for newly installed software or modifications to system files that could indicate further compromise.
- Restore the system from a known good backup if unauthorized changes are detected and cannot be easily reversed. Ensure the backup is clean and free from any malicious alterations.
- Update and patch the system to the latest security standards to close any vulnerabilities that may have been exploited. This includes applying all relevant Windows updates and security patches.
- Enhance monitoring and logging on the affected system and network to detect any similar future attempts. Ensure that all relevant security events are being captured and analyzed.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected. Provide them with all relevant logs and findings for a comprehensive analysis.
