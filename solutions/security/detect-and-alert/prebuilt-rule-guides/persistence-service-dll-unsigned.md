---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unsigned DLL Loaded by Svchost" prebuilt detection rule.
---

# Unsigned DLL Loaded by Svchost

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unsigned DLL Loaded by Svchost

Svchost.exe is a critical Windows process that hosts multiple services, allowing efficient resource management. Adversaries exploit this by loading unsigned DLLs to gain persistence or execute code with elevated privileges. The detection rule identifies such threats by monitoring DLLs recently created and loaded by svchost, focusing on untrusted signatures and unusual file paths, thus highlighting potential malicious activity.

### Possible investigation steps

- Review the specific DLL file path and hash (dll.path and dll.hash.sha256) to determine if it is known to be associated with legitimate software or if it is potentially malicious.
- Check the creation time of the DLL (dll.Ext.relative_file_creation_time) to understand the timeline of events and correlate it with other activities on the system around the same time.
- Investigate the process that loaded the DLL (process.executable) to determine if it is a legitimate instance of svchost.exe or if it has been tampered with or replaced.
- Analyze the code signature status (dll.code_signature.trusted and dll.code_signature.status) to verify if the DLL is unsigned or has an untrusted signature, which could indicate tampering or a malicious origin.
- Cross-reference the DLL's hash (dll.hash.sha256) against known malware databases or threat intelligence sources to identify if it is associated with known threats.
- Examine the system for other indicators of compromise, such as unusual network activity or additional suspicious files, to assess the scope of potential malicious activity.
- Consider isolating the affected system to prevent further potential compromise while conducting a deeper forensic analysis.

### False positive analysis

- System maintenance or updates may trigger the rule by loading legitimate unsigned DLLs. Users can create exceptions for known update processes or maintenance activities to prevent unnecessary alerts.
- Custom or in-house applications might load unsigned DLLs from unusual paths. Verify the legitimacy of these applications and consider adding their specific paths to the exclusion list if they are deemed safe.
- Security or monitoring tools might use unsigned DLLs for legitimate purposes. Identify these tools and exclude their associated DLLs by hash or path to reduce false positives.
- Temporary files created by legitimate software in monitored directories can be mistaken for threats. Regularly review and update the exclusion list to include hashes of these known benign files.
- Development environments often generate unsigned DLLs during testing phases. Ensure that development paths are excluded from monitoring to avoid false alerts during software development cycles.

### Response and remediation

- Isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate the svchost.exe process that loaded the unsigned DLL to stop any ongoing malicious actions.
- Remove the identified unsigned DLL from the system to eliminate the immediate threat.
- Conduct a full antivirus and anti-malware scan on the affected system to detect and remove any additional threats.
- Review and restore any modified system configurations or settings to their original state to ensure system integrity.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for svchost.exe and DLL loading activities to detect similar threats in the future.
