---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "SSH Authorized Keys File Deletion" prebuilt detection rule.'
---

# SSH Authorized Keys File Deletion

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating SSH Authorized Keys File Deletion

SSH authorized keys files are crucial for secure, password-less authentication on Linux systems, storing public keys that grant access. Adversaries may delete these files to disrupt legitimate access or cover their tracks. The detection rule identifies unauthorized deletions by monitoring file removal events, excluding benign processes, thus highlighting potential defense evasion tactics.

### Possible investigation steps

- Review the alert details to identify the specific file name (authorized_keys or authorized_keys2) and the host where the deletion occurred.
- Examine the process that triggered the deletion event, focusing on the process.executable field to determine if it is a known benign process or potentially malicious.
- Check the user account associated with the process that deleted the file to assess if it is a legitimate user or potentially compromised.
- Investigate recent login attempts and SSH access logs on the affected host to identify any unauthorized access or anomalies around the time of the file deletion.
- Look for any other suspicious activities or alerts on the same host that might indicate a broader attack or compromise, such as other file deletions or modifications.
- Assess the impact of the deletion by determining if legitimate access was disrupted and if any critical operations were affected.

### False positive analysis

- Routine system maintenance or updates may trigger deletions of authorized_keys files. To handle this, identify and exclude processes related to scheduled maintenance tasks from the detection rule.
- Automated configuration management tools like Ansible or Puppet might remove and recreate authorized_keys files as part of their operations. Consider excluding these tools' processes if they are verified as non-threatening.
- Cloud service agents, such as those from Google Cloud, may modify SSH keys as part of their operations. Ensure that processes like /usr/bin/google_guest_agent are excluded to prevent false positives.
- Container management services like Docker and containerd might interact with SSH keys during container lifecycle events. Exclude these processes if they are part of legitimate container operations.
- Custom scripts or applications that manage SSH keys for legitimate purposes should be reviewed and, if necessary, added to the exclusion list to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or potential lateral movement by the attacker.
- Verify the integrity of the SSH configuration and authorized keys files on the affected system. Restore the deleted authorized_keys or authorized_keys2 files from a secure backup if available.
- Conduct a thorough review of recent user and process activity on the affected system to identify any unauthorized access or suspicious behavior that may have led to the deletion.
- Change SSH keys and credentials for all users on the affected system to prevent unauthorized access using potentially compromised keys.
- Implement additional monitoring on the affected system to detect any further unauthorized file deletions or suspicious activities, ensuring that alerts are configured for immediate response.
- Escalate the incident to the security operations team for further investigation and to determine if the attack is part of a larger campaign targeting the organization.
- Review and update access controls and permissions on the affected system to ensure that only authorized users and processes can modify critical files like authorized_keys.
