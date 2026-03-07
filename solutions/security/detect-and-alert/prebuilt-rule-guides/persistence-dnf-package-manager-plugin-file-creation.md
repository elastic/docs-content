---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "DNF Package Manager Plugin File Creation" prebuilt detection rule.'
---

# DNF Package Manager Plugin File Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating DNF Package Manager Plugin File Creation

DNF, a package manager for Fedora-based Linux systems, manages software installations and updates. It uses plugins to extend functionality, which can be targeted by attackers to insert malicious code, ensuring persistence and evasion. The detection rule monitors file creation in plugin directories, excluding legitimate processes, to identify unauthorized modifications indicative of potential backdoor activities.

### Possible investigation steps

- Review the file creation event details, focusing on the file path to confirm if it matches the monitored plugin directories: "/usr/lib/python*/site-packages/dnf-plugins/*" or "/etc/dnf/plugins/*".
- Identify the process responsible for the file creation by examining the process.executable field, ensuring it is not one of the legitimate processes listed in the exclusion criteria.
- Check the file extension of the newly created file to ensure it is not one of the excluded extensions like "swp", "swpx", or "swx".
- Investigate the origin and legitimacy of the process by reviewing its parent process and command line arguments to determine if it aligns with expected behavior.
- Correlate the event with any recent changes or updates in the system that might explain the file creation, such as package installations or system updates.
- Search for any additional suspicious activity or anomalies in the system logs around the time of the alert to identify potential indicators of compromise.
- If the file creation is deemed suspicious, consider isolating the affected system and conducting a deeper forensic analysis to assess the scope and impact of the potential threat.

### False positive analysis

- Legitimate software updates or installations may trigger file creation events in the DNF plugin directories. Users can mitigate this by ensuring that the processes involved in these updates are included in the exclusion list of the detection rule.
- System maintenance scripts or automated tasks that modify or create files in the plugin directories can be mistaken for malicious activity. To handle this, identify these scripts and add their executables to the exclusion list.
- Temporary files created by text editors or system processes, such as those with extensions like "swp", "swpx", or "swx", can be excluded by ensuring these extensions are part of the rule's exclusion criteria.
- Custom scripts or tools that interact with DNF plugins for legitimate purposes should be reviewed and, if deemed safe, their executables should be added to the exclusion list to prevent false positives.
- Processes running from directories like "/nix/store/*" or "/var/lib/dpkg/*" may be part of legitimate package management activities. Users should verify these processes and include them in the exclusion list if they are non-threatening.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the attacker.
- Conduct a thorough review of the newly created or modified files in the DNF plugin directories to identify any malicious code or unauthorized changes.
- Remove any identified malicious files or code from the DNF plugin directories to eliminate the backdoor and restore the integrity of the package manager.
- Revert any unauthorized changes to the system configuration or software settings to their original state using verified backups or system snapshots.
- Update all system packages and plugins to the latest versions to patch any vulnerabilities that may have been exploited by the attacker.
- Monitor the affected system and network for any signs of continued unauthorized access or suspicious activity, using enhanced logging and alerting mechanisms.
- Escalate the incident to the appropriate internal security team or external cybersecurity experts for further investigation and to ensure comprehensive remediation.
