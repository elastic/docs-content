---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Yum Package Manager Plugin File Creation" prebuilt detection rule.
---

# Yum Package Manager Plugin File Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Yum Package Manager Plugin File Creation

The Yum package manager is integral to managing software on Fedora-based Linux systems, utilizing plugins to extend its functionality. Adversaries may exploit this by inserting malicious code into these plugins, ensuring persistent access whenever Yum is executed. The detection rule identifies suspicious file creation in plugin directories, excluding legitimate processes and temporary files, to flag potential unauthorized modifications.

### Possible investigation steps

- Review the file creation event details, focusing on the file path to confirm if it matches the plugin directories "/usr/lib/yum-plugins/*" or "/etc/yum/pluginconf.d/*".
- Identify the process responsible for the file creation by examining the process.executable field, ensuring it is not one of the legitimate processes listed in the exclusion criteria.
- Check the file extension and name to ensure it is not a temporary or excluded file type, such as those with extensions "swp", "swpx", "swx", or names starting with ".ansible".
- Investigate the origin and legitimacy of the process by correlating with other system logs or using threat intelligence to determine if the process is known to be associated with malicious activity.
- Assess the file content for any signs of malicious code or unauthorized modifications, especially if the file is a script or configuration file.
- Determine if there have been any recent changes or updates to the system that could explain the file creation, such as legitimate software installations or updates.

### False positive analysis

- Legitimate software updates or installations may trigger file creation events in Yum plugin directories. To handle these, users can create exceptions for known package management processes like rpm, dnf, and yum, which are already included in the rule's exclusion list.
- Temporary files created by text editors or system processes, such as those with extensions like swp, swpx, or swx, can be safely excluded as they are typically non-threatening. Ensure these extensions are part of the exclusion criteria.
- Automation tools like Ansible may generate temporary files in the plugin directories. Users can exclude file names starting with .ansible or .ansible_tmp to prevent false positives from these operations.
- Processes running from specific directories like /nix/store or /var/lib/dpkg are often part of legitimate system operations. Users should verify these paths and include them in the exclusion list if they are part of regular system behavior.
- System maintenance scripts or tools like sed and perl may create temporary files during their execution. Users can exclude these specific process names and file patterns to reduce false alerts.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes that may be running as a result of the malicious plugin modification to halt any ongoing malicious activity.
- Restore the compromised plugin files from a known good backup to ensure the integrity of the Yum package manager's functionality.
- Conduct a thorough review of user accounts and permissions on the affected system to identify and remove any unauthorized access or privilege escalations.
- Implement file integrity monitoring on the Yum plugin directories to detect any future unauthorized modifications promptly.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected.
- Update and patch the system to the latest security standards to mitigate any vulnerabilities that may have been exploited by the adversary.
