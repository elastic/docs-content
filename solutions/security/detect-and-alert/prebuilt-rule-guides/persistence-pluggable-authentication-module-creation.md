---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Pluggable Authentication Module or Configuration Creation" prebuilt detection rule.
---

# Pluggable Authentication Module or Configuration Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Pluggable Authentication Module or Configuration Creation

Pluggable Authentication Modules (PAM) are integral to Linux systems, managing authentication tasks. Adversaries may exploit PAM by creating or altering its modules or configurations to gain persistence or capture credentials. The detection rule identifies suspicious activities by monitoring file operations in PAM directories, excluding legitimate processes, thus highlighting potential unauthorized modifications.

### Possible investigation steps

- Review the file path and extension to determine if the modified or created file is a PAM shared object or configuration file, focusing on paths like "/lib/security/*", "/etc/pam.d/*", and "/etc/security/pam_*".
- Identify the process executable responsible for the file operation and verify if it is listed as an excluded legitimate process, such as "/bin/dpkg" or "/usr/bin/yum". If not, investigate the process further.
- Check the process execution history and command line arguments to understand the context of the file operation and assess if it aligns with typical system administration tasks.
- Investigate the user account associated with the process to determine if it has legitimate access and permissions to modify PAM files, and check for any signs of compromise or misuse.
- Examine recent system logs and security alerts for any related suspicious activities or anomalies that might indicate a broader attack or compromise.
- If the file operation is deemed suspicious, consider restoring the original PAM configuration from a known good backup and monitor the system for any further unauthorized changes.

### False positive analysis

- Package management operations: Legitimate package managers like dpkg, rpm, and yum may trigger the rule during software updates or installations. To handle this, exclude these processes by adding them to the exception list in the rule configuration.
- System updates and maintenance: Processes such as pam-auth-update and systemd may modify PAM configurations during routine system updates. Exclude these processes to prevent false positives.
- Temporary files: Files with extensions like swp, swpx, and swx are often temporary and not indicative of malicious activity. Exclude these extensions to reduce noise.
- Development environments: Paths like /nix/store/* and /snap/* may be used in development or containerized environments. Consider excluding these paths if they are part of a known and secure setup.
- Automated scripts: Scripts using tools like sed or perl may create temporary files that match the rule's criteria. Exclude these specific patterns if they are part of regular, non-malicious operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Review the specific PAM module or configuration file that was created or modified to understand the changes made and assess the potential impact on system security.
- Restore the affected PAM files from a known good backup to ensure the integrity of the authentication process and remove any malicious modifications.
- Conduct a thorough scan of the system using updated antivirus and anti-malware tools to identify and remove any additional malicious software that may have been introduced.
- Monitor the system and network for any signs of continued unauthorized access or suspicious activity, focusing on the indicators of compromise related to PAM manipulation.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if other systems may be affected.
- Implement additional monitoring and alerting for PAM-related activities to enhance detection capabilities and prevent similar threats in the future.
