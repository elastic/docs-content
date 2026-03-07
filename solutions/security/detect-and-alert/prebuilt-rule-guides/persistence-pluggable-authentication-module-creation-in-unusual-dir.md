---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Pluggable Authentication Module (PAM) Creation in Unusual Directory" prebuilt detection rule.'
---

# Pluggable Authentication Module (PAM) Creation in Unusual Directory

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Pluggable Authentication Module (PAM) Creation in Unusual Directory

Pluggable Authentication Modules (PAM) are integral to Linux systems, managing authentication tasks. Adversaries may exploit PAM by creating malicious modules in non-standard directories, aiming to gain persistence or capture credentials. The detection rule identifies such anomalies by monitoring the creation of PAM files outside typical system paths, excluding benign processes and known directories, thus highlighting potential threats.

### Possible investigation steps

- Review the file creation event details, focusing on the file path and name to determine the exact location and nature of the PAM shared object file created.
- Investigate the process that created the file by examining the process name and its parent process to understand the context and legitimacy of the file creation.
- Check the user account associated with the process that created the file to assess if it has the necessary permissions and if the activity aligns with typical user behavior.
- Analyze recent system logs and command history for any suspicious activities or commands that might indicate an attempt to compile or move PAM modules.
- Correlate the event with other security alerts or anomalies on the system to identify potential patterns or coordinated actions that could indicate a broader compromise.
- If possible, retrieve and analyze the contents of the PAM shared object file to identify any malicious code or indicators of compromise.

### False positive analysis

- Development and testing environments may compile PAM modules in temporary directories. To manage this, exclude paths commonly used for development, such as "/tmp/dev/*" or "/var/tmp/test/*".
- Containerized applications might create PAM modules in non-standard directories. Exclude processes like "dockerd" and "containerd" to prevent false positives from container operations.
- Package managers or system update tools may temporarily store PAM modules in unusual directories during updates. Exclude paths like "/var/cache/pacman/pkg/*" or "/var/lib/dpkg/tmp.ci/*" to avoid alerts during legitimate system updates.
- Custom scripts or automation tools might generate PAM modules in user-specific directories. Identify and exclude these specific scripts or paths if they are known to be safe and necessary for operations.
- Temporary backup or recovery operations might involve copying PAM modules to non-standard locations. Exclude paths used for backups, such as "/backup/*" or "/recovery/*", if these operations are verified as secure.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Conduct a thorough review of the unusual directory where the PAM file was created to identify any other suspicious files or activities, and remove any malicious files found.
- Analyze the process that created the PAM file to determine if it was initiated by a legitimate user or process, and terminate any malicious processes.
- Reset credentials for any accounts that may have been compromised, focusing on those with elevated privileges or access to sensitive systems.
- Restore the affected system from a known good backup to ensure that no malicious modifications persist.
- Implement additional monitoring on the affected system and similar systems to detect any further attempts to create PAM files in unusual directories.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
