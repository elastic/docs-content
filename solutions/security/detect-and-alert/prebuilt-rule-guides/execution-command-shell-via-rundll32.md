---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Command Shell Activity Started via RunDLL32" prebuilt detection rule.'
---

# Command Shell Activity Started via RunDLL32

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Command Shell Activity Started via RunDLL32

RunDLL32 is a legitimate Windows utility used to execute functions in DLLs, often leveraged by attackers to run malicious code stealthily. Adversaries exploit it to launch command shells like cmd.exe or PowerShell, bypassing security controls. The detection rule identifies such abuse by monitoring for command shells initiated by RunDLL32, excluding known benign patterns, thus highlighting potential threats.

### Possible investigation steps

- Review the process details to confirm the parent-child relationship between rundll32.exe and the command shell (cmd.exe or powershell.exe) to ensure the alert is not a false positive.
- Examine the command line arguments of rundll32.exe to identify any suspicious or unusual DLLs or functions being executed, excluding known benign patterns.
- Check the user account associated with the process to determine if it aligns with expected behavior or if it indicates potential compromise.
- Investigate the source and destination network connections associated with the process to identify any suspicious or unauthorized communication.
- Correlate the event with other security alerts or logs from the same host or user to identify any patterns or additional indicators of compromise.
- Review recent changes or activities on the host, such as software installations or updates, that might explain the execution of rundll32.exe with command shells.

### False positive analysis

- Known false positives include command shells initiated by RunDLL32 for legitimate administrative tasks or software installations.
- Exclude command lines that match common benign patterns, such as those involving SHELL32.dll or temporary files used by trusted applications.
- Regularly update the list of exceptions to include new benign patterns identified through monitoring and analysis.
- Collaborate with IT and security teams to identify and document legitimate use cases of RunDLL32 in your environment.
- Use process monitoring tools to verify the legitimacy of command shells started by RunDLL32, ensuring they align with expected behavior.

### Response and remediation

- Isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes identified as cmd.exe or powershell.exe that were initiated by rundll32.exe to halt potential malicious actions.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malicious files or remnants.
- Review and analyze the rundll32.exe command line arguments to understand the scope and intent of the activity, and identify any additional compromised systems or accounts.
- Reset credentials for any user accounts that were active on the affected system during the time of the alert to prevent unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for rundll32.exe and related processes to detect similar activities in the future and improve response times.
