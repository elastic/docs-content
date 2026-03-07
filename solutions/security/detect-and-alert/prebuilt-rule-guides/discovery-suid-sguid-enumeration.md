---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "SUID/SGUID Enumeration Detected" prebuilt detection rule.'
---

# SUID/SGUID Enumeration Detected

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating SUID/SGUID Enumeration Detected

In Linux, SUID and SGID permissions allow programs to execute with elevated privileges, potentially exposing systems to privilege escalation if misconfigured. Adversaries exploit this by searching for binaries with these permissions to gain unauthorized access. The detection rule identifies suspicious use of the "find" command to locate such binaries, flagging potential misuse by monitoring specific command arguments and execution contexts.

### Possible investigation steps

- Review the process execution details to confirm the use of the "find" command with SUID/SGID permission arguments by checking the process.name and process.args fields.
- Identify the user and group context in which the command was executed by examining the user.Ext.real.id and group.Ext.real.id fields to determine if the command was run by a non-root user.
- Analyze the command's arguments to understand the scope of the search, focusing on the process.args field to see if specific directories or files were targeted.
- Check for any other suspicious activities or commands executed by the same user or process around the same time to identify potential follow-up actions or privilege escalation attempts.
- Investigate the system for any newly created or modified files with SUID/SGID permissions that could indicate successful privilege escalation or preparation for future attacks.

### False positive analysis

- System administrators or security tools may use the find command with SUID/SGID arguments for legitimate audits. To handle this, create exceptions for known administrative users or specific scripts that regularly perform these checks.
- Automated scripts or cron jobs might execute the find command with these arguments as part of routine maintenance tasks. Identify these scripts and exclude them from monitoring by specifying their process paths or user IDs.
- Some legitimate software installations or updates might temporarily use the find command with SUID/SGID arguments. Monitor installation logs and exclude these processes by correlating them with known software update activities.
- Developers or testers might use the find command in development environments to test security configurations. Exclude these environments from the rule by specifying their hostnames or IP addresses in the exception list.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule, particularly those involving the "find" command with SUID/SGID arguments.
- Conduct a thorough review of the system's SUID/SGID binaries to identify any misconfigurations or unauthorized changes. Remove or correct permissions on any binaries that are not required to have elevated privileges.
- Implement additional monitoring on the affected system to detect any further attempts to exploit SUID/SGID binaries, focusing on process execution and permission changes.
- Escalate the incident to the security operations team for a deeper forensic analysis to determine the scope of the compromise and identify any other affected systems.
- Apply patches and updates to the system and any vulnerable applications to mitigate known vulnerabilities that could be exploited through SUID/SGID binaries.
- Review and enhance access controls and privilege management policies to minimize the risk of privilege escalation through misconfigured binaries in the future.
