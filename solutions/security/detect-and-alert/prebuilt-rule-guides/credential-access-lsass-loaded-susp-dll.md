---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Module Loaded by LSASS" prebuilt detection rule.
---

# Suspicious Module Loaded by LSASS

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Module Loaded by LSASS

The Local Security Authority Subsystem Service (LSASS) is crucial for managing security policies and handling user authentication in Windows environments. Adversaries exploit LSASS by loading malicious or untrusted DLLs to access sensitive credentials. The detection rule identifies such threats by monitoring LSASS for unsigned or untrusted DLLs, excluding known safe signatures and hashes, thus flagging potential credential dumping activities.

### Possible investigation steps

- Review the process details for lsass.exe to confirm the presence of any unsigned or untrusted DLLs loaded into the process. Pay particular attention to the DLL's code signature status and hash values.
- Cross-reference the identified DLL's hash against known malicious hashes in threat intelligence databases to determine if it is associated with any known threats.
- Investigate the source and path of the suspicious DLL to understand how it was introduced into the system. This may involve checking recent file creation or modification events in the system directories.
- Analyze the system's event logs for any related activities or anomalies around the time the suspicious DLL was loaded, such as unusual user logins or privilege escalation attempts.
- Check for any recent changes in the system's security settings or policies that might have allowed the loading of untrusted DLLs into LSASS.
- If the DLL is confirmed to be malicious, isolate the affected system to prevent further credential access or lateral movement within the network.

### False positive analysis

- Legitimate software from trusted vendors not included in the exclusion list may trigger false positives. Users can update the exclusion list with additional trusted signatures or hashes from verified vendors to prevent these alerts.
- Custom or in-house developed DLLs used within the organization might be flagged as suspicious. Organizations should ensure these DLLs are signed with a trusted certificate and add their signatures to the exclusion list if necessary.
- Security software updates or patches from vendors not currently listed may cause false positives. Regularly review and update the exclusion list to include new trusted signatures from security software providers.
- Temporary or expired certificates for legitimate DLLs can result in false positives. Users should verify the legitimacy of these DLLs and update the exclusion list with their signatures if they are confirmed safe.
- DLLs from newly installed software that are not yet recognized as trusted may be flagged. Users should validate the software's source and add its signatures to the exclusion list if it is deemed secure.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate the LSASS process if it is confirmed to be running a malicious or untrusted DLL, ensuring that this action does not disrupt critical services.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malicious files or remnants.
- Review and reset credentials for any accounts that may have been compromised, focusing on those with elevated privileges.
- Implement application whitelisting to prevent unauthorized DLLs from being loaded into critical processes like LSASS in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Update security monitoring tools to enhance detection capabilities for similar threats, ensuring that alerts are generated for any future attempts to load untrusted DLLs into LSASS.
