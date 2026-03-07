---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Upgrade of Non-interactive Shell" prebuilt detection rule.
---

# Potential Upgrade of Non-interactive Shell

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Upgrade of Non-interactive Shell

In Linux environments, attackers often seek to enhance a basic reverse shell to a fully interactive shell to gain a more robust foothold. This involves using tools like `stty` or `script` to manipulate terminal settings, enabling features like command history and job control. The detection rule identifies such activities by monitoring specific process executions and arguments, flagging potential misuse indicative of an upgrade attempt.

### Possible investigation steps

- Review the process execution details to confirm the presence of `stty` or `script` commands with the specific arguments outlined in the detection rule, such as `stty raw -echo` or `script -qc /dev/null`.
- Examine the parent process of the flagged `stty` or `script` command to determine how the shell was initially spawned and identify any potentially malicious scripts or binaries.
- Check the user account associated with the process execution to assess if it aligns with expected user behavior or if it indicates potential compromise.
- Investigate the network connections associated with the host at the time of the alert to identify any suspicious remote connections that could be indicative of a reverse shell.
- Review historical process execution and login records for the user and host to identify any patterns of suspicious activity or previous attempts to establish a reverse shell.

### False positive analysis

- System administrators or legitimate users may use stty or script commands for routine maintenance or troubleshooting, which can trigger the rule. To manage this, create exceptions for known user accounts or specific maintenance windows.
- Automated scripts or cron jobs that utilize stty or script for legitimate purposes might be flagged. Review these scripts and whitelist them by process hash or command line pattern to prevent false positives.
- Development environments where developers frequently use stty or script for testing purposes can generate alerts. Consider excluding specific development machines or user groups from the rule to reduce noise.
- Monitoring tools or security solutions that simulate shell upgrades for testing or auditing purposes may inadvertently trigger the rule. Identify these tools and add them to an exception list based on their process name or execution path.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or lateral movement by the attacker.
- Terminate any suspicious processes identified by the detection rule, specifically those involving `stty` or `script` with the flagged arguments, to disrupt the attacker's attempt to upgrade the shell.
- Conduct a thorough review of the affected system's logs and process history to identify any additional malicious activities or compromised accounts.
- Reset credentials for any user accounts that were active during the time of the alert to prevent unauthorized access using potentially compromised credentials.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited by the attacker.
- Enhance monitoring and logging on the affected host and similar systems to detect any future attempts to upgrade non-interactive shells or other suspicious activities.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems may be affected.
