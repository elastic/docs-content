---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential OpenSSH Backdoor Logging Activity" prebuilt detection rule.'
---

# Potential OpenSSH Backdoor Logging Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential OpenSSH Backdoor Logging Activity

OpenSSH is a widely used protocol for secure remote administration and file transfers. Adversaries may exploit OpenSSH by modifying its binaries to log credentials or maintain unauthorized access. The detection rule identifies suspicious file changes linked to SSH processes, focusing on unusual file names, extensions, and paths indicative of backdoor activity, thus helping to uncover potential security breaches.

### Possible investigation steps

- Review the file change event details to identify the specific file name, extension, and path involved in the alert. Pay particular attention to unusual file names or extensions and paths listed in the query, such as "/usr/lib/*.so.*" or "/private/etc/ssh/.sshd_auth".
- Examine the process executable that triggered the alert, either "/usr/sbin/sshd" or "/usr/bin/ssh", to determine if it has been modified or replaced. Check the integrity of these binaries using hash comparisons against known good versions.
- Investigate the user account associated with the process that made the file change. Determine if the account has a history of suspicious activity or if it has been compromised.
- Check for any recent or unusual login attempts or sessions related to the SSH service on the host. Look for patterns that might indicate unauthorized access or credential harvesting.
- Analyze system logs, such as auth.log or secure.log, for any anomalies or entries that coincide with the time of the file change event. This can provide additional context or evidence of malicious activity.
- If a backdoor is suspected, consider isolating the affected system from the network to prevent further unauthorized access and begin remediation efforts, such as restoring from a clean backup or reinstalling the affected services.

### False positive analysis

- Routine system updates or package installations may trigger file changes in SSH-related directories. Users can create exceptions for known update processes to prevent false alerts.
- Custom scripts or administrative tasks that modify SSH configuration files for legitimate purposes might be flagged. Users should whitelist these scripts or processes if they are verified as non-malicious.
- Backup or synchronization tools that create temporary files with unusual extensions or names in SSH directories can cause false positives. Exclude these tools from monitoring if they are part of regular operations.
- Development or testing environments where SSH binaries are frequently modified for testing purposes may generate alerts. Implement exclusions for these environments to reduce noise.
- Automated configuration management tools like Ansible or Puppet that modify SSH settings as part of their operations can be excluded if they are part of authorized workflows.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious SSH processes identified in the alert to halt potential backdoor activity.
- Conduct a thorough review of the modified files and binaries, particularly those listed in the query, to assess the extent of the compromise and identify any malicious code or unauthorized changes.
- Restore affected files and binaries from a known good backup to ensure system integrity and remove any backdoor modifications.
- Change all SSH credentials and keys associated with the compromised system to prevent unauthorized access using potentially logged credentials.
- Implement additional monitoring on the affected system and network for any signs of persistence or further malicious activity, focusing on the paths and file types highlighted in the detection query.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected, ensuring a coordinated response to the threat.
