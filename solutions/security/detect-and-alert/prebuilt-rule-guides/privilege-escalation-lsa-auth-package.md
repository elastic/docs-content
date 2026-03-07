---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential LSA Authentication Package Abuse" prebuilt detection rule.'
---

# Potential LSA Authentication Package Abuse

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential LSA Authentication Package Abuse

The Local Security Authority (LSA) in Windows manages authentication and security policies. Adversaries exploit LSA by modifying registry paths to include malicious binaries, which are executed with SYSTEM privileges during authentication package loading. The detection rule identifies unauthorized registry changes by non-SYSTEM users, signaling potential privilege escalation or persistence attempts.

### Possible investigation steps

- Review the registry change event details to identify the specific binary path added to the LSA Authentication Packages registry key.
- Investigate the user account associated with the registry change event to determine if it is a legitimate user or potentially compromised.
- Check the timestamp of the registry modification to correlate with any other suspicious activities or events on the system around the same time.
- Analyze the binary referenced in the registry change for any known malicious signatures or behaviors using antivirus or threat intelligence tools.
- Examine system logs and security events for any signs of privilege escalation or persistence techniques used by the adversary.
- Assess the system for any additional unauthorized changes or indicators of compromise that may suggest further malicious activity.

### False positive analysis

- Legitimate software installations or updates may modify the LSA authentication package registry path. Users should verify if recent installations or updates coincide with the detected changes and consider excluding these specific software processes if they are deemed safe.
- System administrators or IT management tools might perform authorized changes to the registry for maintenance or configuration purposes. Users can create exceptions for known administrative tools or processes that are regularly used for legitimate system management tasks.
- Security software or endpoint protection solutions may alter the registry as part of their normal operation. Users should identify and whitelist these security applications to prevent unnecessary alerts.
- Custom scripts or automation tools used within the organization might inadvertently trigger this rule. Users should review and document these scripts, ensuring they are secure, and exclude them if they are confirmed to be non-threatening.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious processes associated with the unauthorized registry change to halt potential malicious activity.
- Restore the modified registry path to its original state by removing any unauthorized entries in the LSA Authentication Packages registry key.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malicious binaries or remnants.
- Review and reset credentials for any accounts that may have been compromised, focusing on those with elevated privileges.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for registry changes, particularly those involving LSA authentication packages, to detect and respond to similar threats in the future.
