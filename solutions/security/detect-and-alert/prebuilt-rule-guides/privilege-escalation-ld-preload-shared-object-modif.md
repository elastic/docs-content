---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Modification of Dynamic Linker Preload Shared Object" prebuilt detection rule.'
---

# Modification of Dynamic Linker Preload Shared Object

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Modification of Dynamic Linker Preload Shared Object

The dynamic linker preload mechanism in Linux, via `/etc/ld.so.preload`, allows preloading of shared libraries, influencing how executables load dependencies. Adversaries exploit this by inserting malicious libraries, hijacking execution flow for privilege escalation. The detection rule monitors changes to this file, excluding benign processes, to identify unauthorized modifications indicative of such abuse.

### Possible investigation steps

- Review the alert details to confirm the file path involved is /etc/ld.so.preload and verify the event action is one of the specified actions: updated, renamed, or file_rename_event.
- Identify the process responsible for the modification by examining the process.name field, ensuring it is not one of the excluded processes (wine or oneagentinstallaction).
- Investigate the process that triggered the alert by gathering additional context such as process ID, command line arguments, and parent process to understand its origin and purpose.
- Check the modification timestamp and correlate it with other system events or logs to identify any suspicious activity or patterns around the time of the modification.
- Analyze the contents of /etc/ld.so.preload to determine if any unauthorized or suspicious libraries have been added, and assess their potential impact on the system.
- Review user accounts and permissions associated with the process to determine if there has been any unauthorized access or privilege escalation attempt.
- If malicious activity is confirmed, isolate the affected system and follow incident response procedures to mitigate the threat and prevent further exploitation.

### False positive analysis

- Legitimate software installations or updates may modify /etc/ld.so.preload. To handle this, monitor the process names associated with these activities and consider adding them to the exclusion list if they are verified as benign.
- System management tools like configuration management software might update /etc/ld.so.preload as part of routine operations. Identify these tools and exclude their process names from the detection rule to prevent false alerts.
- Custom scripts or administrative tasks executed by trusted users could inadvertently trigger the rule. Review these scripts and, if necessary, exclude their process names or user accounts from the detection criteria.
- Security agents or monitoring tools that interact with system files might cause false positives. Verify these tools' activities and exclude their process names if they are known to be safe and necessary for system operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further exploitation or lateral movement by the adversary.
- Terminate any suspicious processes that are not part of the baseline or known benign applications, especially those related to the modification of `/etc/ld.so.preload`.
- Restore the `/etc/ld.so.preload` file from a known good backup to ensure no malicious libraries are preloaded.
- Conduct a thorough review of recent system changes and installed packages to identify any unauthorized software or modifications that may have facilitated the attack.
- Escalate the incident to the security operations team for a deeper forensic analysis to determine the scope of the compromise and identify any additional affected systems.
- Implement additional monitoring on the affected system and similar environments to detect any further attempts to modify the dynamic linker preload file.
- Review and enhance access controls and permissions on critical system files like `/etc/ld.so.preload` to prevent unauthorized modifications in the future.
