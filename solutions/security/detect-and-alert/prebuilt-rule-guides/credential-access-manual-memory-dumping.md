---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Manual Memory Dumping via Proc Filesystem" prebuilt detection rule.
---

# Manual Memory Dumping via Proc Filesystem

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Manual Memory Dumping via Proc Filesystem

The proc filesystem in Linux is a virtual interface providing detailed insights into system processes and their memory. Adversaries exploit this by manually dumping memory from processes to extract sensitive data like credentials. The detection rule identifies suspicious activities by monitoring process executions that access memory files within the proc directory, flagging potential credential access attempts.

### Possible investigation steps

- Review the alert details to identify the specific process name and command line that triggered the rule, focusing on processes like "cat", "grep", "tail", "less", "more", "egrep", or "fgrep" accessing "/proc/*/mem".
- Examine the process execution context, including the parent process and user account associated with the suspicious activity, to determine if the activity is expected or potentially malicious.
- Check the system logs and historical data for any previous occurrences of similar activities involving the same process names and command lines to assess if this is part of a pattern or anomaly.
- Investigate the user account's recent activities and permissions to determine if there are any signs of compromise or unauthorized access that could explain the memory dumping attempt.
- Analyze network traffic and connections from the host to identify any potential data exfiltration attempts or communications with known malicious IP addresses or domains.
- If necessary, isolate the affected system to prevent further potential data leakage and conduct a deeper forensic analysis to uncover any additional indicators of compromise.

### False positive analysis

- System administrators or automated scripts may legitimately access the proc filesystem for monitoring or debugging purposes. To handle this, identify and whitelist known scripts or administrative tools that frequently access memory files.
- Security tools or monitoring solutions might access the proc filesystem as part of their regular operations. Review and exclude these processes from the rule to prevent unnecessary alerts.
- Developers or testers might use commands like cat or grep on proc files during application debugging. Establish a list of approved users or groups who are allowed to perform these actions and exclude their activities from triggering alerts.
- Backup or system maintenance processes could involve accessing proc files. Document these processes and create exceptions for them to avoid false positives.
- Regular system health checks might involve accessing memory files. Identify these checks and configure the rule to ignore them by specifying the associated process names or command patterns.

### Response and remediation

- Immediately isolate the affected system to prevent further unauthorized access or data exfiltration. Disconnect the network connection and disable remote access capabilities.
- Terminate any suspicious processes identified by the detection rule, specifically those accessing memory files within the proc directory using commands like "cat", "grep", "tail", "less", "more", "egrep", or "fgrep".
- Conduct a memory analysis on the isolated system to identify any extracted sensitive data, such as credentials or encryption keys, and assess the extent of the compromise.
- Change all potentially compromised credentials and encryption keys immediately, prioritizing those associated with critical systems and services.
- Review and enhance system logging and monitoring configurations to ensure comprehensive visibility into process activities, particularly those involving the proc filesystem.
- Escalate the incident to the security operations center (SOC) or relevant cybersecurity team for further investigation and to determine if the threat is part of a larger attack campaign.
- Implement additional security controls, such as restricting access to the proc filesystem and employing application whitelisting, to prevent unauthorized memory dumping activities in the future.

