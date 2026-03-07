---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual SSHD Child Process" prebuilt detection rule.
---

# Unusual SSHD Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual SSHD Child Process

Secure Shell (SSH) is a protocol used to securely access remote systems. Adversaries may exploit SSH to maintain persistence or create backdoors by spawning unexpected child processes. The detection rule identifies anomalies by monitoring process creation events where SSH or SSHD is the parent, focusing on atypical command-line arguments, which may indicate malicious activity.

### Possible investigation steps

- Review the process command line arguments for the unusual SSHD child process to identify any suspicious or unexpected commands that could indicate malicious activity.
- Check the user account associated with the SSHD child process to determine if it is a legitimate user or if there are signs of compromise, such as unusual login times or locations.
- Investigate the parent process (SSH or SSHD) to understand the context of the connection, including the source IP address and any associated user activity, to assess if it aligns with expected behavior.
- Examine the process tree to identify any subsequent processes spawned by the unusual SSHD child process, which may provide further insight into the attacker's actions or objectives.
- Correlate the event with other security logs and alerts from the same host or network segment to identify any related suspicious activities or patterns that could indicate a broader attack campaign.

### False positive analysis

- Legitimate administrative scripts or automation tools may trigger this rule if they execute commands with SSH or SSHD as the parent process. To handle this, identify and document these scripts, then create exceptions for their specific command-line patterns.
- System maintenance tasks or updates that involve SSH connections might appear as unusual child processes. Regularly review and whitelist these known maintenance activities to prevent unnecessary alerts.
- Custom user environments or shell configurations that deviate from standard shells like bash, zsh, or sh could be flagged. Analyze these configurations and exclude them if they are verified as non-threatening.
- Monitoring tools or security solutions that interact with SSH sessions for logging or auditing purposes might generate alerts. Verify these tools' behavior and exclude their processes if they are part of legitimate monitoring activities.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious SSHD child processes identified by the alert to halt potential malicious activities.
- Conduct a thorough review of SSH configuration files and access logs to identify unauthorized changes or access patterns, and revert any unauthorized modifications.
- Change all SSH keys and credentials associated with the compromised system to prevent further unauthorized access.
- Implement additional monitoring on the affected system and related network segments to detect any further suspicious activities or attempts to re-establish persistence.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if other systems may be affected.
- Review and update firewall rules and access controls to restrict SSH access to only trusted IP addresses and users, reducing the attack surface for future incidents.
