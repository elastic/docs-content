---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Executable Masquerading as Kernel Process" prebuilt detection rule.'
---

# Executable Masquerading as Kernel Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Executable Masquerading as Kernel Process

In Linux environments, kernel processes like `kthreadd` and `kworker` typically run without associated executable paths. Adversaries exploit this by naming malicious executables after these processes to evade detection. The detection rule identifies anomalies by flagging kernel-named processes with non-empty executable fields, indicating potential masquerading attempts. This helps in uncovering stealthy threats that mimic legitimate system activities.

### Possible investigation steps

- Review the process details for the flagged process, focusing on the process.executable field to identify the path and name of the executable. This can provide initial insights into whether the executable is legitimate or potentially malicious.
- Check the process's parent process (process.parent) to understand the context in which the process was started. This can help determine if the process was spawned by a legitimate system process or a suspicious one.
- Investigate the file at the path specified in the process.executable field. Verify its legitimacy by checking its hash against known malware databases or using a file reputation service.
- Examine the process's command line arguments (process.command_line) for any unusual or suspicious parameters that might indicate malicious activity.
- Review recent system logs and events around the time the process was started to identify any related activities or anomalies that could provide additional context or evidence of compromise.
- If available, use threat intelligence sources to check for any known indicators of compromise (IOCs) related to the process name or executable path.

### False positive analysis

- Custom scripts or administrative tools may be named similarly to kernel processes for convenience or organizational standards. Review these scripts and tools to ensure they are legitimate and consider adding them to an exception list if verified.
- Some legitimate software or monitoring tools might use kernel-like names for their processes to integrate closely with system operations. Verify the source and purpose of these processes and exclude them if they are confirmed to be non-malicious.
- System updates or patches might temporarily create processes with kernel-like names that have executable paths. Monitor these occurrences and exclude them if they are part of a verified update process.
- Development or testing environments may intentionally use kernel-like names for process simulation. Ensure these environments are isolated and add exceptions for these processes if they are part of controlled testing scenarios.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of the potential threat and to contain any malicious activity.
- Terminate the suspicious process immediately to stop any ongoing malicious actions. Use process management tools to kill the process identified by the alert.
- Conduct a forensic analysis of the affected system to identify any additional indicators of compromise (IOCs) and assess the extent of the intrusion.
- Remove any malicious executables or files associated with the masquerading process from the system to ensure complete remediation.
- Restore the system from a known good backup if the integrity of the system is compromised, ensuring that the backup is free from any malicious artifacts.
- Update and patch the system to close any vulnerabilities that may have been exploited by the attacker, ensuring all software and security tools are up to date.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
