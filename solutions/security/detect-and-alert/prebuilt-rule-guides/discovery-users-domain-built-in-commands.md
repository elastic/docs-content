---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Enumeration of Users or Groups via Built-in Commands" prebuilt detection rule.'
---

# Enumeration of Users or Groups via Built-in Commands

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Enumeration of Users or Groups via Built-in Commands

Built-in macOS commands like `ldapsearch`, `dsmemberutil`, and `dscl` are essential for managing and querying user and group information. Adversaries exploit these to gather insights into system accounts and groups, aiding in lateral movement or privilege escalation. The detection rule identifies suspicious use of these commands, especially when executed from non-standard parent processes, excluding known legitimate applications, to flag potential misuse.

### Possible investigation steps

- Review the process details to identify the specific command executed, focusing on the process name and arguments, such as "ldapsearch", "dsmemberutil", or "dscl" with specific arguments like "read", "list", or "search".
- Examine the parent process information, including the executable path and name, to determine if the command was launched from a non-standard or suspicious parent process.
- Check the exclusion list of known legitimate applications to ensure the alert was not triggered by a benign process, such as those from QualysCloudAgent, Kaspersky, or ESET.
- Investigate the user account associated with the process execution to determine if it aligns with expected behavior or if it indicates potential compromise or misuse.
- Correlate the event with other logs or alerts to identify any patterns of suspicious activity, such as repeated enumeration attempts or other discovery tactics.
- Assess the system's recent activity for signs of lateral movement or privilege escalation attempts that may follow the enumeration of users or groups.

### False positive analysis

- Security and management tools like QualysCloudAgent, Kaspersky Anti-Virus, and ESET Endpoint Security may trigger false positives due to their legitimate use of built-in commands for system monitoring. To mitigate this, add these applications to the exclusion list in the detection rule.
- Development environments such as Xcode might execute these commands during normal operations. If Xcode is frequently triggering alerts, consider excluding its executable path from the rule.
- VPN and network management applications like NordVPN and Zscaler may use these commands for network configuration and user management. Exclude these applications if they are known to be safe and frequently used in your environment.
- Parallels Desktop and similar virtualization software might access user and group information as part of their functionality. If these applications are trusted, add their executable paths to the exclusion list.
- Regular administrative tasks performed by IT personnel using NoMAD or similar tools can also cause false positives. Ensure these tools are excluded if they are part of routine operations.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule, specifically those involving `ldapsearch`, `dsmemberutil`, or `dscl` commands executed from non-standard parent processes.
- Conduct a thorough review of user and group accounts on the affected system to identify any unauthorized changes or additions, and revert any suspicious modifications.
- Reset passwords for all user accounts on the affected system, prioritizing those with administrative privileges, to mitigate potential unauthorized access.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems have been compromised.
- Implement additional monitoring on the affected system and network to detect any further unauthorized enumeration attempts or related suspicious activities.
- Review and update endpoint security configurations to ensure that legitimate applications are properly whitelisted and that unauthorized applications are blocked from executing enumeration commands.
