---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kernel Module Removal" prebuilt detection rule.
---

# Kernel Module Removal

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kernel Module Removal

Kernel modules dynamically extend a Linux kernel's capabilities without rebooting. Adversaries may exploit this by removing modules to disable security features or hide malicious activities. The detection rule identifies suspicious module removal attempts by monitoring processes like `rmmod` or `modprobe` with removal arguments, especially when initiated by common shell environments, indicating potential defense evasion tactics.

### Possible investigation steps

- Review the process details to confirm the execution of `rmmod` or `modprobe` with removal arguments. Check the command line arguments to ensure they match the suspicious activity criteria.
- Identify the parent process of the suspicious activity, focusing on shell environments like `sudo`, `bash`, `dash`, `ash`, `sh`, `tcsh`, `csh`, `zsh`, `ksh`, or `fish`, to understand the context in which the module removal was initiated.
- Investigate the user account associated with the process to determine if the activity aligns with expected behavior or if it indicates potential unauthorized access.
- Check system logs and audit logs for any preceding or subsequent suspicious activities that might correlate with the module removal attempt, such as privilege escalation or other defense evasion tactics.
- Assess the impact of the module removal on system security features and functionality, and determine if any critical security modules were targeted.
- Review recent changes or updates to the system that might explain the module removal, such as legitimate maintenance or updates, to rule out false positives.

### False positive analysis

- Routine administrative tasks may trigger the rule when system administrators use `rmmod` or `modprobe` for legitimate maintenance. To handle this, create exceptions for specific user accounts or scripts known to perform these tasks regularly.
- Automated scripts or configuration management tools that manage kernel modules might cause false positives. Identify these tools and exclude their processes from the rule to prevent unnecessary alerts.
- Some Linux distributions or custom setups might use shell scripts that invoke `rmmod` or `modprobe` during system updates or package installations. Monitor these activities and whitelist the associated parent processes if they are verified as non-threatening.
- Development environments where kernel module testing is frequent can generate alerts. Exclude specific development machines or user accounts involved in module testing to reduce noise.
- Security tools that perform regular checks or updates on kernel modules might inadvertently trigger the rule. Verify these tools and add them to the exception list to avoid false positives.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or potential lateral movement by the adversary.
- Terminate any suspicious processes identified as attempting to remove kernel modules, such as those initiated by `rmmod` or `modprobe` with removal arguments.
- Conduct a thorough review of user accounts and privileges on the affected system to ensure no unauthorized access or privilege escalation has occurred.
- Restore any disabled security features or kernel modules to their original state to ensure the system's defenses are intact.
- Analyze system logs and audit trails to identify any additional indicators of compromise or related malicious activities.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the threat is part of a larger attack campaign.
- Implement enhanced monitoring and alerting for similar activities across the network to detect and respond to future attempts promptly.
