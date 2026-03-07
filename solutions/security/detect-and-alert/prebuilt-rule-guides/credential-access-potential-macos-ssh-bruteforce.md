---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential macOS SSH Brute Force Detected" prebuilt detection rule.'
---

# Potential macOS SSH Brute Force Detected

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential macOS SSH Brute Force Detected

SSH (Secure Shell) is a protocol used to securely access remote systems. On macOS, the `sshd-keygen-wrapper` process is involved in SSH key generation. Adversaries may exploit this by repeatedly attempting to generate keys to gain unauthorized access, a tactic known as brute force. The detection rule identifies unusual activity by monitoring for excessive executions of this process, indicating potential brute force attempts.

### Possible investigation steps

- Review the alert details to confirm the host and process information, specifically checking for the host.os.type as macos and the process.name as sshd-keygen-wrapper.
- Examine the frequency and timing of the sshd-keygen-wrapper process executions to determine if they align with normal user activity or if they suggest an automated brute force attempt.
- Investigate the parent process, launchd, to ensure it is legitimate and not being used maliciously to spawn the sshd-keygen-wrapper process.
- Check for any recent successful or failed login attempts on the affected host to identify potential unauthorized access.
- Correlate the activity with any other alerts or logs from the same host to identify patterns or additional indicators of compromise.
- Review user account activity on the host to determine if any accounts have been accessed or modified unexpectedly.

### False positive analysis

- Legitimate administrative tasks may trigger the rule if an administrator is performing routine maintenance or updates that involve generating SSH keys. To handle this, create an exception for known administrative accounts or scheduled maintenance windows.
- Automated scripts or applications that require frequent SSH key generation for legitimate purposes can cause false positives. Identify these scripts or applications and exclude their associated processes or hosts from the detection rule.
- Development environments where SSH keys are frequently generated for testing purposes might trigger the rule. Consider excluding specific development machines or user accounts from the rule to prevent unnecessary alerts.
- Continuous integration/continuous deployment (CI/CD) systems that automate SSH key generation as part of their workflow can be a source of false positives. Exclude these systems or their specific processes from the detection rule to avoid disruption.
- If a known security tool or monitoring system is configured to test SSH key generation as part of its checks, it may trigger the rule. Verify the tool's activity and exclude its processes if deemed non-threatening.

### Response and remediation

- Immediately isolate the affected macOS host from the network to prevent further unauthorized access attempts.
- Terminate any suspicious or unauthorized `sshd-keygen-wrapper` processes running on the affected host to halt ongoing brute force attempts.
- Review and reset SSH credentials for all user accounts on the affected host to ensure no unauthorized access has been achieved.
- Implement IP blocking or rate limiting on the SSH service to prevent further brute force attempts from the same source.
- Conduct a thorough review of the affected host's SSH configuration and logs to identify any unauthorized changes or access.
- Escalate the incident to the security operations team for further investigation and to determine if additional hosts are affected.
- Enhance monitoring and alerting for similar SSH brute force patterns across the network to improve early detection and response capabilities.
