---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Attempt to Clear Kernel Ring Buffer" prebuilt detection rule.
---

# Attempt to Clear Kernel Ring Buffer

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Attempt to Clear Kernel Ring Buffer

The kernel ring buffer logs system messages, crucial for diagnosing issues. Adversaries may clear these logs using the `dmesg -c` command to hide traces of malicious activities, such as installing unauthorized kernel modules. The detection rule identifies this behavior by monitoring the execution of `dmesg` with specific arguments, flagging potential evasion attempts for further investigation.

### Possible investigation steps

- Review the process execution details to confirm the presence of the `dmesg -c` command, focusing on the process name and arguments to ensure the alert is valid.
- Investigate the user account associated with the execution of the `dmesg -c` command to determine if it is a known and authorized user or potentially compromised.
- Check for any recent installations or modifications of Linux kernel modules (LKMs) on the host to identify unauthorized changes that may coincide with the log clearing attempt.
- Examine other system logs and security alerts around the same timeframe to identify any suspicious activities or patterns that may indicate a broader attack or compromise.
- Assess the host's network activity for any unusual outbound connections or data exfiltration attempts that could suggest further malicious intent.

### False positive analysis

- Routine system maintenance activities may trigger the rule if administrators use the dmesg -c command to clear logs for legitimate purposes. To handle this, create exceptions for known maintenance scripts or processes that regularly execute this command.
- Automated scripts or monitoring tools that include dmesg -c as part of their log management routine can cause false positives. Identify these scripts and exclude them from the rule by specifying their process IDs or user accounts.
- Development and testing environments where kernel modules are frequently installed and removed might generate alerts. Consider excluding these environments from the rule or adjusting the risk score to reflect the lower threat level in these contexts.
- System administrators may use dmesg -c during troubleshooting to clear logs and view new messages. Document these activities and create exceptions for specific user accounts or roles that perform this task regularly.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity or lateral movement.
- Conduct a thorough review of the system to identify any unauthorized kernel modules or other suspicious changes, and remove them if found.
- Restore the system from a known good backup if unauthorized changes are detected and cannot be easily reversed.
- Review and update access controls and permissions to ensure that only authorized users have the ability to execute commands like `dmesg -c`.
- Implement enhanced monitoring and logging for the affected system to detect any future attempts to clear the kernel ring buffer or similar evasion tactics.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Conduct a post-incident review to identify gaps in detection and response, and update security policies and procedures to prevent recurrence.
