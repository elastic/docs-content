---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Process Capability Enumeration" prebuilt detection rule.'
---

# Process Capability Enumeration

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Process Capability Enumeration

In Linux environments, the `getcap` command is used to list file capabilities, which define specific privileges for executables. Adversaries may exploit this by recursively scanning the filesystem to identify and manipulate capabilities, potentially escalating privileges. The detection rule identifies suspicious use of `getcap` by monitoring for its execution with specific arguments, especially by non-root users, indicating potential misuse.

### Possible investigation steps

- Review the alert details to confirm the execution of the `getcap` command with the arguments `-r` and `/`, ensuring the process was initiated by a non-root user (user.id != "0").
- Identify the user account associated with the process execution to determine if the user has a legitimate reason to perform such actions.
- Examine the process execution history for the identified user to check for any other suspicious activities or commands executed around the same time.
- Investigate the system logs for any signs of privilege escalation attempts or unauthorized access following the execution of the `getcap` command.
- Check for any recent changes to file capabilities on the system that could indicate manipulation by the adversary.
- Assess the system for any other indicators of compromise or related alerts that might suggest a broader attack campaign.

### False positive analysis

- System administrators or automated scripts may use the getcap command for legitimate auditing purposes. To handle this, create exceptions for known administrative accounts or scripts that regularly perform capability checks.
- Security tools or monitoring solutions might trigger the rule during routine scans. Identify these tools and exclude their processes from triggering alerts by adding them to an allowlist.
- Developers or testing environments may execute getcap as part of software testing or development processes. Exclude specific user IDs or groups associated with these environments to prevent unnecessary alerts.
- Scheduled maintenance tasks might involve capability enumeration. Document and exclude these tasks by specifying the time frames or user accounts involved in the maintenance activities.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further exploitation or lateral movement by the adversary.
- Terminate any unauthorized or suspicious processes associated with the `getcap` command to halt potential privilege escalation activities.
- Conduct a thorough review of the system's file capabilities using a trusted method to identify any unauthorized changes or suspicious capabilities that may have been set.
- Revert any unauthorized capability changes to their original state to ensure that no elevated privileges are retained by malicious users.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement monitoring for similar `getcap` command executions across the environment to detect and respond to future attempts promptly.
- Review and update access controls and user permissions to ensure that only authorized users have the necessary privileges to execute potentially sensitive commands like `getcap`.
