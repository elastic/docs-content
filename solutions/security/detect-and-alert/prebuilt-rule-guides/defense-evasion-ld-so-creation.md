---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Dynamic Linker (ld.so) Creation" prebuilt detection rule.
---

# Dynamic Linker (ld.so) Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Dynamic Linker (ld.so) Creation

The dynamic linker, ld.so, is crucial in Linux environments for loading shared libraries required by executables. Adversaries may exploit this by replacing it with a malicious version to execute unauthorized code, achieving persistence or evading defenses. The detection rule identifies suspicious creation of ld.so files, excluding benign processes, to flag potential threats.

### Possible investigation steps

- Review the process that triggered the alert by examining the process.executable field to understand which application attempted to create the ld.so file.
- Check the process.name field to ensure the process is not one of the benign processes listed in the exclusion criteria, such as "dockerd", "yum", "dnf", "microdnf", or "pacman".
- Investigate the file.path to confirm the location of the newly created ld.so file and verify if it matches any of the specified directories like "/lib", "/lib64", "/usr/lib", or "/usr/lib64".
- Analyze the parent process of the suspicious executable to determine if it was initiated by a legitimate or potentially malicious source.
- Look for any recent changes or anomalies in the system logs around the time of the file creation event to identify any related suspicious activities.
- Cross-reference the event with other security tools or logs, such as Elastic Defend or SentinelOne, to gather additional context or corroborating evidence of malicious activity.
- Assess the risk and impact of the event by considering the system's role and the potential consequences of a compromised dynamic linker on that system.

### False positive analysis

- Package managers like yum, dnf, microdnf, and pacman can trigger false positives when they update or install packages that involve the dynamic linker. These processes are already excluded in the rule, but ensure any custom package managers or scripts are also considered for exclusion.
- Container management tools such as dockerd may create or modify ld.so files during container operations. If you use other container tools, consider adding them to the exclusion list to prevent false positives.
- System updates or maintenance scripts that involve library updates might create ld.so files. Review these scripts and add them to the exclusion list if they are verified as non-threatening.
- Custom administrative scripts or automation tools that interact with shared libraries could inadvertently trigger the rule. Identify these scripts and exclude them if they are part of regular, secure operations.
- Development environments where ld.so files are frequently created or modified during testing and compilation processes may need specific exclusions for development tools or environments to avoid false positives.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Verify the integrity of the dynamic linker (ld.so) on the affected system by comparing it with a known good version from a trusted source or repository.
- If the dynamic linker has been tampered with, replace it with the verified version and ensure all system binaries are intact.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection tools to identify and remove any additional malicious files or processes.
- Review system logs and the process creation history to identify the source of the unauthorized ld.so creation and any associated malicious activity.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if other systems are affected.
- Implement additional monitoring and alerting for similar suspicious activities, such as unauthorized file creations in critical system directories, to enhance future detection capabilities.
