---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Remote SSH Login Enabled via systemsetup Command" prebuilt detection rule.
---

# Remote SSH Login Enabled via systemsetup Command

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Remote SSH Login Enabled via systemsetup Command

The `systemsetup` command in macOS is a utility that allows administrators to configure system settings, including enabling remote SSH login, which facilitates remote management and access. Adversaries may exploit this to gain unauthorized access and move laterally within a network. The detection rule identifies suspicious use of `systemsetup` to enable SSH, excluding legitimate administrative tools, by monitoring process execution patterns and arguments.

### Possible investigation steps

- Review the process execution details to confirm the use of the systemsetup command with the arguments "-setremotelogin" and "on" to ensure the alert is not a false positive.
- Check the parent process of the systemsetup command to identify if it was executed by a known administrative tool or script, excluding /usr/local/jamf/bin/jamf as per the rule.
- Investigate the user account associated with the process execution to determine if it is a legitimate administrator or a potentially compromised account.
- Examine recent login events and SSH access logs on the host to identify any unauthorized access attempts or successful logins following the enabling of remote SSH login.
- Correlate this event with other security alerts or logs from the same host or network segment to identify potential lateral movement or further malicious activity.

### False positive analysis

- Legitimate administrative tools like Jamf may trigger this rule when enabling SSH for authorized management purposes. To handle this, ensure that the process parent executable path for Jamf is correctly excluded in the detection rule.
- Automated scripts used for system configuration and maintenance might enable SSH as part of their routine operations. Review these scripts and, if verified as safe, add their parent process paths to the exclusion list.
- IT support activities that require temporary SSH access for troubleshooting can also cause false positives. Document these activities and consider scheduling them during known maintenance windows to reduce alerts.
- Security software or management tools that periodically check or modify system settings could inadvertently trigger this rule. Identify these tools and exclude their specific process paths if they are confirmed to be non-threatening.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious or unauthorized SSH sessions that are currently active on the affected system.
- Review and revoke any unauthorized SSH keys or credentials that may have been added to the system.
- Conduct a thorough examination of the system logs to identify any additional unauthorized activities or changes made by the adversary.
- Restore the system to a known good state from a backup taken before the unauthorized SSH access was enabled, if possible.
- Implement network segmentation to limit SSH access to only trusted administrative systems and users.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems have been compromised.
