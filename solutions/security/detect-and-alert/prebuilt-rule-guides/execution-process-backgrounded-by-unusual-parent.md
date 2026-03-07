---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Process Backgrounded by Unusual Parent" prebuilt detection rule.'
---

# Process Backgrounded by Unusual Parent

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Process Backgrounded by Unusual Parent

In Linux environments, shell processes like bash or zsh can be backgrounded using the '&' operator, allowing them to run independently of the terminal. Adversaries exploit this by launching scripts with unusual parent processes to evade detection. The detection rule identifies such anomalies by monitoring process start events with specific shell invocations and backgrounding indicators, flagging potential evasion attempts.

### Possible investigation steps

- Review the process start event details to identify the parent process and assess its legitimacy. Pay attention to the process.name and process.args fields to understand the context of the command executed.
- Examine the command line arguments (process.args) for any suspicious patterns or commands that could indicate malicious activity, especially focusing on the use of the '&' operator which backgrounds the process.
- Check the user account associated with the process to determine if it is a known and trusted user. Investigate any anomalies in user behavior or unexpected user accounts.
- Correlate the event with other logs or alerts from the same host to identify any related suspicious activities or patterns, such as other unusual process executions or network connections.
- Investigate the parent process's history and behavior to determine if it has been involved in other suspicious activities or if it has been compromised.
- Consult threat intelligence sources or databases to see if the command or behavior matches known attack patterns or indicators of compromise (IOCs).

### False positive analysis

- Routine administrative scripts may trigger this rule if they are executed with backgrounding by system administrators. To manage this, identify and whitelist known administrative scripts that are frequently used in your environment.
- Automated maintenance tasks or cron jobs that use shell scripts with backgrounding can also be flagged. Review and exclude these tasks by adding exceptions for specific scripts or processes that are verified as non-threatening.
- Development environments where developers frequently test scripts in the background might cause false positives. Consider creating exceptions for specific user accounts or directories where development activities are known to occur.
- Monitoring tools or agents that use shell scripts to perform checks or gather data in the background could be mistakenly identified. Verify these tools and exclude their processes from the rule to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the adversary.
- Terminate the suspicious backgrounded process and its parent process to halt any ongoing malicious activity.
- Conduct a thorough review of the affected system's process tree to identify any additional suspicious or unauthorized processes that may have been spawned.
- Analyze the command history and script files associated with the unusual parent process to understand the scope and intent of the activity.
- Restore the system from a known good backup if any malicious modifications or persistence mechanisms are identified.
- Update and patch the system to close any vulnerabilities that may have been exploited by the adversary.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
