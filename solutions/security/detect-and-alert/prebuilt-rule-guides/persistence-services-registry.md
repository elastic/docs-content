---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Persistence via Services Registry" prebuilt detection rule.
---

# Unusual Persistence via Services Registry

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Persistence via Services Registry

Windows services are crucial for running background processes. Adversaries may exploit this by directly altering service registry keys to maintain persistence, bypassing standard APIs. The detection rule identifies such anomalies by monitoring changes to specific registry paths and filtering out legitimate processes, thus highlighting potential unauthorized service modifications indicative of malicious activity.

### Possible investigation steps

- Review the specific registry paths and values that triggered the alert, focusing on "ServiceDLL" and "ImagePath" within the specified registry paths to identify any unauthorized or suspicious modifications.
- Examine the process responsible for the registry change, paying attention to the process name and executable path, to determine if it is a known legitimate process or potentially malicious.
- Cross-reference the process executable path against the list of known legitimate paths excluded in the query to ensure it is not a false positive.
- Investigate the historical behavior of the process and any associated files or network activity to identify patterns indicative of malicious intent or persistence mechanisms.
- Check for any recent changes or anomalies in the system's service configurations that could correlate with the registry modifications, indicating potential unauthorized service creation or alteration.
- Consult threat intelligence sources or databases to determine if the process or registry changes are associated with known malware or adversary techniques.

### False positive analysis

- Legitimate software installations or updates may modify service registry keys directly. Users can create exceptions for known software update processes by excluding their executables from the detection rule.
- System maintenance tools like Process Explorer may trigger false positives when they interact with service registry keys. Exclude these tools by adding their process names and paths to the exception list.
- Drivers installed by trusted hardware peripherals might alter service registry keys. Users should identify and exclude these driver paths if they are known to be safe and frequently updated.
- Custom enterprise applications that require direct registry modifications for service management can be excluded by specifying their executable paths in the rule exceptions.
- Regular system processes such as svchost.exe or services.exe are already excluded, but ensure any custom scripts or automation tools that mimic these processes are also accounted for in the exceptions.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified in the alert that are not part of legitimate applications or services.
- Restore the modified registry keys to their original state using a known good backup or by manually correcting the entries to ensure the integrity of the service configurations.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any additional malicious software or artifacts.
- Review and update endpoint protection policies to ensure that similar unauthorized registry modifications are detected and blocked in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
- Document the incident details, including the steps taken for containment and remediation, to enhance future response efforts and update threat intelligence databases.
