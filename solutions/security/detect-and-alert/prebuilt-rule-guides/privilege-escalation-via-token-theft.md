---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Process Created with an Elevated Token" prebuilt detection rule.'
---

# Process Created with an Elevated Token

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Process Created with an Elevated Token

In Windows environments, processes can be created with elevated tokens to perform tasks requiring higher privileges. Adversaries exploit this by impersonating system-level binaries to escalate privileges and bypass security controls. The detection rule identifies such activities by monitoring process creation events, focusing on those initiated by privileged binaries and excluding known benign processes. This helps in identifying unauthorized privilege escalation attempts.

### Possible investigation steps

- Review the process creation event details to identify the specific executable and its parent process, focusing on the fields process.executable and process.Ext.effective_parent.executable.
- Check the user.id field to confirm if the process was created with the SYSTEM user ID (S-1-5-18), indicating elevated privileges.
- Investigate the parent process executable path to determine if it matches any known privileged Microsoft native binaries, which could be targets for token theft.
- Examine the process code signature details, especially process.code_signature.trusted and process.code_signature.subject_name, to verify if the executable is signed by a trusted entity or if it matches any excluded signatures.
- Correlate the process creation event with other security logs and alerts to identify any related suspicious activities or patterns that might indicate privilege escalation attempts.
- Assess the context and timing of the event to determine if it aligns with legitimate administrative tasks or if it appears anomalous in the environment.

### False positive analysis

- Utility Manager in Windows running in debug mode can trigger false positives. To handle this, exclude processes where both the effective parent and parent executables are Utilman.exe with the /debug argument.
- Windows print spooler service correlated with Access Intelligent Form may cause false alerts. Exclude processes where the parent executable is spoolsv.exe and the process executable is LaunchCreate.exe under Access Intelligent Form.
- Windows error reporting executables like WerFault.exe can be mistakenly flagged. Exclude these specific executables from the rule to prevent unnecessary alerts.
- Windows updates initiated by TiWorker.exe running with elevated privileges can be misidentified. Exclude processes where TiWorker.exe is the parent and the process executable matches known update-related paths.
- Additional parent executables that typically run with elevated privileges, such as AtBroker.exe and svchost.exe, can lead to false positives. Exclude these parent executables from the rule to reduce noise.
- Trusted Windows binaries with specific signature names, such as those from TeamViewer or Cisco WebEx, may be incorrectly flagged. Exclude processes with a trusted code signature and matching subject names to avoid false alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule that are running with elevated privileges, especially those not matching known benign processes.
- Conduct a thorough review of user accounts and privileges on the affected system to identify and disable any unauthorized accounts or privilege escalations.
- Restore the affected system from a known good backup to ensure any malicious changes are reverted, and verify the integrity of the system post-restoration.
- Implement additional monitoring on the affected system and network to detect any further attempts at privilege escalation or token manipulation.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the threat has spread to other systems.
- Review and update endpoint protection and detection capabilities to ensure they are configured to detect similar threats in the future, leveraging the MITRE ATT&CK framework for guidance on Access Token Manipulation (T1134).
