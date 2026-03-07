---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unsigned DLL Side-Loading from a Suspicious Folder" prebuilt detection rule.
---

# Unsigned DLL Side-Loading from a Suspicious Folder

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unsigned DLL Side-Loading from a Suspicious Folder

DLL side-loading exploits the trust of signed executables to load malicious DLLs, often from suspicious directories. Adversaries use this to bypass security measures by placing unsigned DLLs in locations mimicking legitimate paths. The detection rule identifies this by checking for trusted programs loading recently modified, unsigned DLLs from atypical directories, signaling potential evasion tactics.

### Possible investigation steps

- Review the process code signature to confirm the legitimacy of the trusted program that loaded the DLL. Check if the process is expected to run from the identified directory.
- Examine the DLL's path and creation or modification time to determine if it aligns with typical user or system activity. Investigate why the DLL was recently modified or created.
- Analyze the DLL's code signature status to understand why it is unsigned or has an error status. This can help identify if the DLL is potentially malicious.
- Investigate the parent process and any associated child processes to understand the context of the DLL loading event. This can provide insights into how the DLL was introduced.
- Check for any recent changes or anomalies in the system or user activity logs around the time the DLL was created or modified to identify potential indicators of compromise.
- Correlate the alert with other security events or alerts in the environment to determine if this is part of a broader attack or isolated incident.

### False positive analysis

- Legitimate software updates or installations may temporarily load unsigned DLLs from atypical directories. Users can create exceptions for known update processes by verifying the source and ensuring the process is part of a legitimate update.
- Custom or in-house applications might load unsigned DLLs from non-standard directories. Users should verify the application's behavior and, if deemed safe, exclude these specific paths or processes from the rule.
- Development environments often involve testing unsigned DLLs in various directories. Developers can exclude these environments by specifying the directories or processes involved in the development workflow.
- Some third-party security or system management tools may use unsigned DLLs for legitimate purposes. Users should confirm the tool's legitimacy and add exceptions for these tools to prevent false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of the potential threat and to contain any malicious activity.
- Terminate the process associated with the unsigned DLL to stop any ongoing malicious operations.
- Quarantine the suspicious DLL file and any related files for further analysis to understand the scope and nature of the threat.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or remnants.
- Review and restore any altered system configurations or settings to their original state to ensure system integrity.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the threat has impacted other systems.
- Implement additional monitoring and logging on the affected system and network to detect any recurrence or similar threats in the future.
