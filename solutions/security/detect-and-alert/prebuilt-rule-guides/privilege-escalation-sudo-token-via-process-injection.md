---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Sudo Token Manipulation via Process Injection" prebuilt detection rule.
---

# Potential Sudo Token Manipulation via Process Injection

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Sudo Token Manipulation via Process Injection

In Linux environments, process injection can be exploited by adversaries to manipulate sudo tokens, allowing unauthorized privilege escalation. Attackers may use debugging tools like gdb to inject code into processes with valid sudo tokens, leveraging ptrace capabilities. The detection rule identifies this threat by monitoring for gdb execution followed by a uid change in the sudo process, indicating potential token manipulation.

### Possible investigation steps

- Review the alert details to identify the specific host and process session leader entity ID involved in the potential sudo token manipulation.
- Examine the process tree on the affected host to trace the parent and child processes of the gdb execution, focusing on any unusual or unauthorized processes.
- Check the system logs for any recent sudo commands executed by the user associated with the gdb process to determine if there were any unauthorized privilege escalations.
- Investigate the user account associated with the gdb process to verify if it has legitimate reasons to use debugging tools and if it has been compromised.
- Analyze the timing and context of the uid change event in the sudo process to assess if it aligns with legitimate administrative activities or if it appears suspicious.
- Review the system's ptrace settings to ensure they are configured securely and assess if there have been any recent changes that could have enabled this attack vector.

### False positive analysis

- Debugging activities by developers or system administrators using gdb for legitimate purposes can trigger this rule. To manage this, create exceptions for specific user IDs or groups known to perform regular debugging tasks.
- Automated scripts or maintenance tools that utilize gdb for process analysis might cause false positives. Identify these scripts and exclude their associated process names or paths from the rule.
- System monitoring or security tools that perform uid changes as part of their normal operation could be mistaken for malicious activity. Review and whitelist these tools by their process names or specific user IDs.
- Training or testing environments where sudo and gdb are used frequently for educational purposes may generate alerts. Consider excluding these environments by host ID or network segment to reduce noise.
- Scheduled tasks or cron jobs that involve gdb and sudo processes might inadvertently match the rule criteria. Analyze these tasks and exclude them based on their execution times or specific process attributes.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or privilege escalation.
- Terminate any suspicious gdb and sudo processes identified in the alert to stop ongoing process injection attempts.
- Conduct a thorough review of the affected system's process and user activity logs to identify any unauthorized changes or access patterns.
- Reset credentials and sudo tokens for all users on the affected system to prevent further exploitation using compromised tokens.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Re-enable ptrace restrictions if they were previously disabled, to limit the ability of attackers to perform process injection.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
