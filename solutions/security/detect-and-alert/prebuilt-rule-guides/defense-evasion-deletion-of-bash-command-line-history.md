---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Tampering of Shell Command-Line History" prebuilt detection rule.
---

# Tampering of Shell Command-Line History

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Tampering of Shell Command-Line History

Shell command-line history is a crucial feature in Unix-like systems, recording user commands for convenience and auditing. Adversaries may manipulate this history to hide their tracks, using commands to delete or redirect history files, clear history buffers, or disable history logging. The detection rule identifies such tampering by monitoring for suspicious command patterns and arguments indicative of history manipulation attempts.

### Possible investigation steps

- Review the process execution details to identify the user account associated with the suspicious command, focusing on the process.args field to determine the specific command and arguments used.
- Check the process execution timeline to correlate the suspicious activity with other events on the system, such as logins or file modifications, to understand the context of the tampering attempt.
- Investigate the command history files (.bash_history, .zsh_history) for the affected user accounts to assess the extent of tampering and identify any commands that may have been executed prior to the history manipulation.
- Examine system logs and audit records for any additional indicators of compromise or related suspicious activities, such as unauthorized access attempts or privilege escalation events.
- Verify the current configuration of the HISTFILE and HISTFILESIZE environment variables for the affected user accounts to ensure they have not been altered to disable history logging.

### False positive analysis

- System administrators or automated scripts may clear command-line history as part of routine maintenance or privacy measures. To handle this, identify and whitelist known scripts or user accounts that perform these actions regularly.
- Developers or power users might redirect or unset history files to manage disk space or for personal preference. Consider excluding specific user accounts or directories from monitoring if these actions are verified as non-malicious.
- Security tools or compliance scripts may execute commands that resemble history tampering to ensure systems are in a desired state. Review and exclude these tools from triggering alerts by adding them to an exception list.
- Temporary testing environments or sandboxed systems might frequently clear history as part of their reset processes. Exclude these environments from the rule to prevent unnecessary alerts.
- Users with privacy concerns might intentionally disable history logging. Engage with these users to understand their needs and adjust monitoring policies accordingly, possibly by excluding their sessions from the rule.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further tampering or data exfiltration.
- Conduct a thorough review of the affected user's recent command history and system logs to identify any unauthorized or suspicious activities that may have occurred prior to the tampering.
- Restore the tampered history files from a secure backup, if available, to aid in further forensic analysis and ensure continuity of auditing.
- Re-enable and secure shell history logging by resetting the HISTFILE and HISTFILESIZE environment variables to their default values and ensuring they are not set to null or zero.
- Implement stricter access controls and monitoring on the affected system to prevent unauthorized users from modifying shell history files in the future.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may have been compromised.
- Review and update endpoint detection and response (EDR) configurations to enhance monitoring for similar tampering attempts, ensuring alerts are generated for any future suspicious command patterns.
