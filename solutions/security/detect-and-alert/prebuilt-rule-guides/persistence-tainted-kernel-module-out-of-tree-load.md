---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Tainted Out-Of-Tree Kernel Module Load" prebuilt detection rule.
---

# Tainted Out-Of-Tree Kernel Module Load

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Tainted Out-Of-Tree Kernel Module Load

Kernel modules extend the functionality of the Linux kernel without rebooting the system. While beneficial, out-of-tree modules, not included in the official kernel source, can taint the kernel, posing security risks. Adversaries exploit this by loading malicious modules to evade detection and maintain persistence. The detection rule monitors syslog for specific messages indicating such module loads, helping identify potential threats early.

### Possible investigation steps

- Review the syslog entries around the time of the alert to gather additional context about the module load event, focusing on messages with "loading out-of-tree module taints kernel."
- Identify the specific out-of-tree kernel module that was loaded by examining the syslog message details and cross-reference with known legitimate modules.
- Check the system for any recent changes or installations that might have introduced the out-of-tree module, such as software updates or new applications.
- Investigate the source and integrity of the module by verifying its origin and comparing its hash against known good or malicious hashes.
- Assess the system for any signs of compromise or unauthorized access, focusing on persistence mechanisms and defense evasion tactics, as indicated by the MITRE ATT&CK framework references.
- Consult with system administrators or relevant stakeholders to determine if the module load was authorized or expected as part of normal operations.

### False positive analysis

- Legitimate third-party drivers or hardware support modules may trigger alerts when loaded as out-of-tree modules. Users should verify the source and purpose of these modules to ensure they are not malicious.
- Custom-built modules for specific applications or hardware optimizations can also cause false positives. Users can create exceptions for these modules by adding them to an allowlist if they are verified as safe and necessary for system operations.
- Development and testing environments often load experimental or custom modules that are not part of the official kernel. In such cases, users should document these modules and exclude them from alerts to avoid unnecessary noise.
- Regularly updated or patched modules from trusted vendors might not be immediately recognized as safe. Users should maintain a list of trusted vendors and update their exception lists accordingly to prevent false positives.
- Some security tools or monitoring solutions may use out-of-tree modules for enhanced functionality. Users should ensure these tools are from reputable sources and exclude their modules from detection rules if they are confirmed to be secure.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the adversary.
- Identify and unload the suspicious out-of-tree kernel module using the `rmmod` command to remove it from the kernel.
- Conduct a thorough review of the system's kernel module load history and verify the legitimacy of all loaded modules.
- Perform a comprehensive malware scan on the affected system to detect and remove any additional malicious software.
- Restore the system from a known good backup if the integrity of the system cannot be assured after module removal.
- Implement stricter access controls and monitoring for kernel module loading to prevent unauthorized module loads in the future.
- Escalate the incident to the security operations team for further investigation and to assess the need for broader organizational response measures.
