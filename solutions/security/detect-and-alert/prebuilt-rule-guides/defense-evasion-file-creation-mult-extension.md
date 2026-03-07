---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Executable File Creation with Multiple Extensions" prebuilt detection rule.'
---

# Executable File Creation with Multiple Extensions

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Executable File Creation with Multiple Extensions

In Windows environments, adversaries may exploit file extensions to disguise malicious executables as benign files, such as documents or images, by appending multiple extensions. This tactic, known as masquerading, aims to deceive users and evade security measures. The detection rule identifies suspicious file creations by monitoring for executables with misleading extensions, excluding known legitimate processes, thus highlighting potential threats.

### Possible investigation steps

- Review the file creation event details to identify the full file path and name, focusing on the extensions used to determine if they match the suspicious pattern outlined in the query.
- Investigate the process that created the file by examining the process.executable field to determine if it is a known legitimate process or potentially malicious.
- Check the file's origin by analyzing the user account and network activity associated with the file creation event to identify any unusual or unauthorized access patterns.
- Utilize threat intelligence sources to assess if the file hash or any related indicators of compromise (IOCs) are known to be associated with malicious activity.
- Examine the file's metadata and properties to verify its authenticity and check for any signs of tampering or unusual characteristics.
- Conduct a behavioral analysis of the file in a controlled environment to observe any malicious actions or network communications it may attempt.

### False positive analysis

- Legitimate software installations may create executables with multiple extensions during setup processes. Users can exclude these by adding exceptions for known installer paths, such as "C:\Users\*\QGIS_SCCM\Files\QGIS-OSGeo4W-*-Setup-x86_64.exe".
- System updates or patches might temporarily create files with multiple extensions. Monitor and verify these activities, and if confirmed as legitimate, add exceptions for the specific update processes.
- Development environments or script-based applications may generate files with multiple extensions for testing purposes. Identify these environments and exclude their specific file paths or processes to prevent false positives.
- Security tools or administrative scripts might use multiple extensions for legitimate purposes. Review and whitelist these tools by their executable paths or process names to avoid unnecessary alerts.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of the potential threat and to contain any malicious activity.
- Terminate any suspicious processes associated with the masquerading executable files to halt any ongoing malicious actions.
- Quarantine the identified files with multiple extensions to prevent execution and further analysis.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional threats.
- Review and restore any altered system configurations or files to their original state to ensure system integrity.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for similar file creation activities to improve detection and response capabilities for future incidents.
