---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "SSH Authorized Key File Activity Detected via Defend for Containers" prebuilt detection rule.'
---

# SSH Authorized Key File Activity Detected via Defend for Containers

## Setup

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating SSH Authorized Key File Activity Detected via Defend for Containers

In containerized environments, SSH keys facilitate secure access, but adversaries can exploit this by altering the authorized_keys file to gain unauthorized access. This detection rule identifies suspicious changes to SSH authorized_keys files within containers, signaling potential persistence tactics. By monitoring file modifications, it helps detect unauthorized SSH usage, a common indicator of compromise.

### Possible investigation steps

- Review the container ID associated with the alert to identify the specific container where the modification occurred.
- Examine the timestamp of the event to determine when the file change or creation took place and correlate it with any known activities or changes in the environment.
- Investigate the user account or process that made the modification to the authorized_keys file to assess if it was an authorized action.
- Check for any recent SSH connections to the container, especially those using public key authentication, to identify potential unauthorized access.
- Analyze the contents of the modified authorized_keys file to identify any suspicious or unauthorized keys.
- Review the container's logs and any related network activity around the time of the modification for signs of compromise or lateral movement attempts.

### False positive analysis

- Routine updates or deployments within containers may modify SSH configuration files, leading to false positives. To manage this, create exceptions for known update processes or deployment scripts that regularly alter these files.
- Automated configuration management tools like Ansible or Puppet might change SSH files as part of their normal operation. Identify these tools and exclude their activities from triggering alerts by specifying their process IDs or user accounts.
- Development or testing environments often see frequent changes to SSH keys for legitimate reasons. Consider excluding these environments from the rule or setting up a separate, less sensitive monitoring profile for them.
- Scheduled maintenance tasks that involve SSH key rotation can trigger alerts. Document these tasks and schedule exceptions during their execution windows to prevent unnecessary alerts.
- Container orchestration systems might modify SSH configurations as part of scaling or updating services. Recognize these patterns and adjust the rule to ignore changes made by these systems.

### Response and remediation

- Immediately isolate the affected container to prevent further unauthorized access or lateral movement within the environment.
- Revoke any unauthorized SSH keys found in the authorized_keys file to cut off the adversary's access.
- Conduct a thorough review of all SSH configuration files within the container to ensure no additional unauthorized modifications have been made.
- Restore the container from a known good backup if available, ensuring that the backup does not contain the unauthorized changes.
- Implement stricter access controls and monitoring on SSH usage within containers to prevent similar incidents in the future.
- Escalate the incident to the security operations team for further investigation and to determine if other containers or systems have been compromised.
- Update detection and alerting mechanisms to include additional indicators of compromise related to SSH key manipulation and unauthorized access attempts.
