---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Expired or Revoked Driver Loaded" prebuilt detection rule.
---

# Expired or Revoked Driver Loaded

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Expired or Revoked Driver Loaded
In Windows environments, drivers facilitate communication between the OS and hardware. Adversaries exploit vulnerabilities in outdated drivers or misuse revoked certificates to execute malicious code in kernel mode, bypassing security controls. The detection rule identifies such threats by monitoring for drivers with expired or revoked signatures, focusing on processes critical to system integrity, thus flagging potential privilege escalation or defense evasion attempts.

### Possible investigation steps

- Review the alert details to confirm the presence of a driver with an expired or revoked signature, focusing on the process with PID 4, which is typically the System process in Windows.
- Investigate the specific driver file that triggered the alert by checking its file path, hash, and any associated metadata to determine its origin and legitimacy.
- Cross-reference the driver file against known vulnerability databases and security advisories to identify any known exploits associated with it.
- Examine recent system logs and security events for any unusual activities or attempts to load other drivers around the same time as the alert.
- Assess the system for any signs of privilege escalation or defense evasion, such as unauthorized access attempts or changes to security settings.
- If the driver is confirmed to be malicious or suspicious, isolate the affected system to prevent further compromise and initiate a detailed forensic analysis.

### False positive analysis

- Legitimate software updates may load drivers with expired or revoked signatures temporarily. Verify the source and purpose of the driver before excluding it.
- Some older hardware devices may rely on drivers that have expired signatures but are still necessary for functionality. Confirm the device's necessity and consider excluding these drivers if they are from a trusted source.
- Security software or system management tools might use drivers with expired signatures for legitimate operations. Validate the software's legitimacy and add exceptions for these drivers if they are verified as safe.
- Custom or in-house developed drivers might not have updated signatures. Ensure these drivers are from a trusted internal source and consider excluding them if they are essential for operations.
- Test environments may intentionally use expired or revoked drivers for research or development purposes. Clearly document these cases and exclude them to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further exploitation or lateral movement by the adversary.
- Terminate any processes associated with the expired or revoked driver to halt any ongoing malicious activity.
- Conduct a thorough review of the system to identify any unauthorized changes or additional malicious drivers that may have been loaded.
- Revoke any compromised certificates and update the certificate trust list to prevent future misuse.
- Apply the latest security patches and driver updates to close any vulnerabilities that may have been exploited.
- Restore the system from a known good backup if any unauthorized changes or persistent threats are detected.
- Escalate the incident to the security operations center (SOC) for further analysis and to determine if additional systems are affected.
