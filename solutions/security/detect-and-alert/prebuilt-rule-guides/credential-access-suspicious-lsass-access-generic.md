---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Lsass Process Access" prebuilt detection rule.
---

# Suspicious Lsass Process Access

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Lsass Process Access

The Local Security Authority Subsystem Service (LSASS) is crucial for enforcing security policies and managing user logins in Windows environments. Adversaries often target LSASS to extract credentials, enabling unauthorized access. The detection rule identifies unusual access attempts to LSASS by filtering out legitimate processes and access patterns, focusing on anomalies that suggest credential dumping activities.

### Possible investigation steps

- Review the process details that triggered the alert, focusing on the process name and executable path to determine if it is a known legitimate application or potentially malicious.
- Examine the GrantedAccess value in the event data to understand the level of access attempted on the LSASS process and compare it against typical access patterns.
- Investigate the parent process of the suspicious process to identify how it was spawned and assess if it is part of a legitimate workflow or an anomaly.
- Check the CallTrace field for any unusual or suspicious DLLs that might indicate malicious activity or exploitation attempts.
- Correlate the alert with other security events or logs from the same host to identify any related suspicious activities or patterns, such as network connections or file modifications.
- Verify the host's security posture, including the status of antivirus or endpoint protection solutions, to ensure they are functioning correctly and have not been tampered with.

### False positive analysis

- Legitimate security tools like Sysinternals Process Explorer and Process Monitor can trigger false positives. Exclude these by adding their process names to the exception list.
- Windows Defender and other antivirus software may access LSASS for legitimate scanning purposes. Exclude their executable paths from the detection rule to prevent false alerts.
- System processes such as csrss.exe, lsm.exe, and wmiprvse.exe are known to access LSASS as part of normal operations. Ensure these are included in the process executable exceptions to avoid unnecessary alerts.
- Software updates and installers, like those from Cisco AnyConnect or Oracle, may access LSASS during legitimate operations. Add these specific paths to the exclusion list to reduce false positives.
- Custom enterprise applications that interact with LSASS for authentication purposes should be identified and their paths added to the exceptions to prevent disruption in monitoring.

### Response and remediation

- Isolate the affected system from the network immediately to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified in the alert that are attempting to access the LSASS process, ensuring that legitimate processes are not disrupted.
- Conduct a memory dump analysis of the affected system to identify any malicious tools or scripts used for credential dumping, focusing on the LSASS process.
- Change all potentially compromised credentials, especially those with administrative privileges, to prevent unauthorized access using stolen credentials.
- Apply patches and updates to the affected system to address any vulnerabilities that may have been exploited by the adversary.
- Monitor the network for any signs of further suspicious activity or attempts to access LSASS on other systems, using enhanced logging and alerting mechanisms.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
