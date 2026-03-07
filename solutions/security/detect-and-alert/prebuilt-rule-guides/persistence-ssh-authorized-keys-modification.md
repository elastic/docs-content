---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "SSH Authorized Keys File Activity" prebuilt detection rule.'
---

# SSH Authorized Keys File Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating SSH Authorized Keys File Activity

SSH authorized_keys files are crucial for secure, password-less authentication, allowing users to log into servers using public keys. Adversaries exploit this by adding their keys, ensuring persistent access. The detection rule identifies unauthorized changes to these files, excluding benign processes, to flag potential threats, focusing on persistence and lateral movement tactics.

### Possible investigation steps

- Review the alert details to identify the specific file that was modified, focusing on "authorized_keys", "authorized_keys2", "/etc/ssh/sshd_config", or "/root/.ssh".
- Examine the process that triggered the alert by checking the process executable path to ensure it is not one of the benign processes listed in the exclusion criteria.
- Investigate the user account associated with the modification to determine if it is a legitimate user or potentially compromised.
- Check the timestamp of the file modification to correlate with any known user activity or scheduled tasks that might explain the change.
- Analyze recent login attempts and SSH connections to the server to identify any suspicious activity or unauthorized access.
- Review the contents of the modified authorized_keys file to identify any unfamiliar or unauthorized public keys that have been added.
- If unauthorized keys are found, remove them and consider resetting credentials or keys for affected accounts to prevent further unauthorized access.

### False positive analysis

- Development tools like git and maven may modify SSH authorized_keys files during legitimate operations. To prevent these from triggering alerts, add their paths to the exclusion list in the detection rule.
- System utilities such as vim and touch are often used by administrators to manually update authorized_keys files. Consider excluding these processes if they are part of regular maintenance activities.
- Automation tools like puppet and chef-client might update SSH configurations as part of their deployment scripts. Verify these changes are expected and exclude these processes if they are part of routine operations.
- Docker-related processes may alter SSH configurations when containers are being managed. If these changes are part of standard container operations, include the relevant paths in the exclusion list.
- Google Guest Agent and JumpCloud Agent might modify SSH settings as part of their management tasks. Confirm these actions are legitimate and exclude these processes if they align with normal system management activities.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or lateral movement.
- Review the SSH authorized_keys file and remove any unauthorized or suspicious public keys that have been added.
- Change the passwords for all user accounts on the affected host to prevent adversaries from regaining access using compromised credentials.
- Conduct a thorough review of user accounts and permissions on the affected host to identify and disable any unauthorized accounts or privilege escalations.
- Restore the affected system from a known good backup if unauthorized changes are extensive or if the integrity of the system is in question.
- Implement additional monitoring on the affected host and network to detect any further unauthorized access attempts or suspicious activities.
- Escalate the incident to the security operations team for further investigation and to determine if other systems may be affected.
