---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Interactive Terminal Spawned via Perl" prebuilt detection rule.
---

# Interactive Terminal Spawned via Perl

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Interactive Terminal Spawned via Perl

Perl, a versatile scripting language, can execute system commands, making it a target for adversaries seeking to escalate privileges or maintain persistence. Attackers may exploit Perl to spawn interactive terminals, transforming basic shells into robust command interfaces. The detection rule identifies such activity by monitoring process events on Linux systems, specifically when Perl executes shell commands, signaling potential misuse.

### Possible investigation steps

- Review the process event logs to confirm the presence of a Perl process with arguments indicating the execution of a shell, such as "exec \"/bin/sh\";", "exec \"/bin/dash\";", or "exec \"/bin/bash\";".
- Identify the user account associated with the Perl process to determine if it aligns with expected activity or if it suggests unauthorized access.
- Examine the parent process of the Perl execution to understand how the Perl script was initiated and assess if it correlates with legitimate user activity or a potential compromise.
- Check for any network connections or data transfers initiated by the Perl process to identify possible exfiltration or communication with external command and control servers.
- Investigate any recent changes to user accounts, permissions, or scheduled tasks that might indicate privilege escalation or persistence mechanisms associated with the Perl activity.
- Correlate the event with other security alerts or logs from the same host to identify patterns or additional indicators of compromise that could suggest a broader attack campaign.

### False positive analysis

- System maintenance scripts that use Perl to execute shell commands may trigger this rule. Review and whitelist known maintenance scripts by adding exceptions for specific script paths or process arguments.
- Automated deployment tools that utilize Perl for executing shell commands can cause false positives. Identify these tools and exclude their specific process arguments or execution paths from the detection rule.
- Development environments where Perl is used for testing or debugging purposes might inadvertently spawn interactive terminals. Consider excluding processes initiated by known development user accounts or within specific development directories.
- Backup or monitoring scripts that rely on Perl to perform system checks or data collection could be flagged. Analyze these scripts and create exceptions based on their unique process arguments or execution context.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious Perl processes identified by the detection rule to halt any ongoing malicious activity.
- Conduct a thorough review of the affected system's logs and process history to identify any additional indicators of compromise or related malicious activity.
- Reset credentials and review access permissions for any accounts that may have been compromised or used in the attack.
- Restore the affected system from a known good backup to ensure any malicious changes are removed.
- Implement additional monitoring on the affected host and network to detect any further attempts to exploit Perl for spawning interactive terminals.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if broader organizational impacts exist.
