---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kernel Unpacking Activity" prebuilt detection rule.'
---

# Kernel Unpacking Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kernel Unpacking Activity

Kernel unpacking involves using utilities to extract or inspect kernel images and modules, often for legitimate maintenance or updates. However, adversaries exploit this to identify vulnerabilities or alter the kernel for malicious purposes. The detection rule identifies suspicious unpacking by monitoring specific Linux utilities and command patterns, excluding benign processes like system updates, to flag potential threats.

### Possible investigation steps

- Review the process details to identify the specific utility used for unpacking, such as "file", "unlzma", "gunzip", etc., and verify if the usage aligns with typical system maintenance activities.
- Examine the parent process name and arguments, especially those involving "/boot/*", to determine if the unpacking activity is part of a legitimate system operation or an unauthorized action.
- Check the user account associated with the process to assess if the activity was initiated by a legitimate user or an unauthorized entity.
- Investigate the timing of the event to see if it coincides with scheduled maintenance or updates, which might explain the unpacking activity.
- Look for any related alerts or logs that might indicate further suspicious behavior, such as attempts to modify kernel modules or other system files following the unpacking activity.
- Cross-reference the event with recent system updates or patches to rule out false positives related to legitimate system operations.

### False positive analysis

- System updates and maintenance activities can trigger this rule when legitimate processes unpack kernel images. To manage this, exclude processes initiated by known update utilities like "mkinitramfs" from triggering alerts.
- Custom scripts or administrative tasks that involve unpacking kernel images for legitimate purposes may also cause false positives. Identify and whitelist these scripts or processes by their specific command patterns or parent process names.
- Backup or recovery operations that involve accessing or unpacking kernel files might be flagged. Review these operations and exclude them by specifying the responsible process names or arguments in the detection rule.
- Automated security tools that scan or analyze kernel images for compliance or vulnerability assessments can be mistaken for malicious activity. Exclude these tools by adding their process names to the exception list.

### Response and remediation

- Isolate the affected system from the network to prevent potential lateral movement or further exploitation by the adversary.
- Terminate any suspicious processes identified by the detection rule, especially those involving the unpacking of kernel images or modules.
- Conduct a thorough review of the system's kernel and module integrity using trusted tools to ensure no unauthorized modifications have been made.
- Restore the system from a known good backup if any unauthorized changes to the kernel or system files are detected.
- Update the system's kernel and all related packages to the latest versions to mitigate any known vulnerabilities that could be exploited.
- Monitor the system for any recurring suspicious activity, focusing on the use of utilities and command patterns identified in the detection rule.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
