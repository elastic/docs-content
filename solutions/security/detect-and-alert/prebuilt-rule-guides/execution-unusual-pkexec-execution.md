---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Pkexec Execution" prebuilt detection rule.'
---

# Unusual Pkexec Execution

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Pkexec Execution

`Pkexec` is a command-line utility in Linux environments that allows users to execute commands as another user, often with elevated privileges. Adversaries may exploit `pkexec` to escalate privileges or execute unauthorized actions by invoking it through shell processes. The detection rule identifies atypical `pkexec` executions initiated by common shell interpreters, flagging potential misuse by monitoring specific process attributes and execution patterns.

### Possible investigation steps

- Review the process tree to understand the context of the pkexec execution, focusing on the parent process names such as bash, dash, sh, tcsh, csh, zsh, ksh, or fish, as these are indicative of shell-based invocations.
- Examine the command-line arguments passed to pkexec to determine the intended action and assess whether it aligns with expected administrative tasks or appears suspicious.
- Check the user account associated with the pkexec execution to verify if the account has legitimate reasons to perform such actions, and investigate any anomalies in user behavior or account activity.
- Investigate the timing and frequency of the pkexec executions to identify patterns or correlations with other suspicious activities or known attack timelines.
- Cross-reference the alert with other security logs and alerts from data sources like Elastic Endgame, Elastic Defend, Crowdstrike, or SentinelOne to gather additional context and corroborate findings.
- Assess the system's current state for signs of compromise, such as unauthorized changes, unexpected network connections, or the presence of known malicious files or processes.

### False positive analysis

- Routine administrative tasks: System administrators may use pkexec for legitimate purposes, such as performing maintenance tasks. To handle this, create exceptions for known administrator accounts or specific maintenance scripts that regularly invoke pkexec.
- Automated scripts: Some automated scripts or cron jobs might use pkexec to perform scheduled tasks. Identify these scripts and exclude their specific process names or paths from the rule to prevent false alerts.
- Software updates: Certain software update processes might use pkexec to apply patches or updates. Monitor and document these processes, then configure exceptions for recognized update mechanisms.
- Development environments: Developers might use pkexec during testing or development. Establish a list of development machines or user accounts and exclude them from the rule to reduce noise.
- Custom user applications: Users may have custom applications that require pkexec for legitimate functionality. Review these applications and whitelist their specific execution patterns to avoid unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the adversary.
- Terminate any suspicious `pkexec` processes identified by the alert to halt unauthorized actions or privilege escalation attempts.
- Review and analyze the parent shell process and its command history to understand the context and origin of the `pkexec` execution.
- Reset credentials and review permissions for the user accounts involved to mitigate any unauthorized access or privilege escalation.
- Conduct a thorough scan of the affected system for additional indicators of compromise or persistence mechanisms that may have been deployed.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Update and enhance monitoring rules to detect similar `pkexec` misuse attempts in the future, ensuring comprehensive coverage of shell processes and privilege escalation activities.
