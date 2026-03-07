---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Microsoft Antimalware Service Execution" prebuilt detection rule.'
---

# Suspicious Microsoft Antimalware Service Execution

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Microsoft Antimalware Service Execution

The Microsoft Antimalware Service Executable, a core component of Windows Defender, is crucial for real-time protection against malware. Adversaries exploit its trust by renaming it or executing it from non-standard paths to load malicious DLLs, bypassing security measures. The detection rule identifies such anomalies by monitoring process names and paths, flagging deviations from expected behavior to uncover potential threats.

### Possible investigation steps

- Review the process details to confirm if the process name is MsMpEng.exe but is executing from a non-standard path. Check the process.executable field to identify the exact path and verify if it deviates from the expected directories.
- Investigate the parent process of the suspicious MsMpEng.exe instance to determine how it was initiated. This can provide insights into whether the process was started by a legitimate application or a potentially malicious one.
- Examine the system for any recent file modifications or creations in the directory where the suspicious MsMpEng.exe is located. This can help identify if a malicious DLL was recently placed in the same directory.
- Check for any network connections or communications initiated by the suspicious MsMpEng.exe process. This can help determine if the process is attempting to communicate with external servers, which may indicate malicious activity.
- Look for any other processes or activities on the host that may indicate compromise, such as unusual user account activity or other processes running from unexpected locations. This can help assess the broader impact of the potential threat.

### False positive analysis

- Legitimate software updates or installations may temporarily rename or relocate the Microsoft Antimalware Service Executable. Users should verify if any software updates or installations occurred around the time of the alert and consider excluding these paths if they are known and trusted.
- Custom security or IT management tools might execute the executable from non-standard paths for monitoring or testing purposes. Confirm with IT or security teams if such tools are in use and add these paths to the exclusion list if they are verified as safe.
- Virtualization or sandbox environments may replicate the executable in different locations for testing or analysis. Check if the environment is part of a controlled setup and exclude these paths if they are part of legitimate operations.
- Backup or recovery processes might involve copying the executable to alternate locations. Ensure these processes are legitimate and consider excluding these paths if they are part of routine operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further spread of the potential threat.
- Terminate any suspicious processes identified by the detection rule, specifically those involving MsMpEng.exe running from non-standard paths.
- Conduct a thorough scan of the affected system using an updated antivirus or endpoint detection and response (EDR) tool to identify and remove any malicious DLLs or other malware.
- Review and restore any altered or deleted system files from a known good backup to ensure system integrity.
- Investigate the source of the DLL side-loading attempt to determine if it was part of a broader attack campaign, and gather forensic evidence for further analysis.
- Escalate the incident to the security operations center (SOC) or incident response team for a deeper investigation and to assess the need for further containment measures.
- Implement additional monitoring and alerting for similar anomalies in process execution paths to enhance detection capabilities and prevent recurrence.
