---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Symbolic Link Created" prebuilt detection rule.
---

# Suspicious Symbolic Link Created

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Symbolic Link Created

Symbolic links in Linux are shortcuts that point to files or directories, facilitating easy access. Adversaries may exploit these links to redirect privileged processes to sensitive files, potentially escalating privileges or accessing restricted data. The detection rule identifies suspicious link creation by monitoring the execution of the 'ln' command with specific arguments and targets, especially when initiated by non-root users, indicating potential misuse.

### Possible investigation steps

- Review the process details to confirm the execution of the 'ln' command with suspicious arguments such as "-s" or "-sf" and verify the target files or directories listed in the query, like "/etc/shadow" or "/bin/bash".
- Check the user and group IDs associated with the process to ensure they are not root (ID "0"), as the rule specifically targets non-root users.
- Investigate the parent process name to determine if it is one of the shell processes listed in the query, such as "bash" or "zsh", which might indicate a user-initiated action.
- Examine the working directory and arguments to identify if the symbolic link creation is targeting sensitive locations like "/etc/cron.d/*" or "/home/*/.ssh/*".
- Analyze the user's recent activity and command history to understand the context and intent behind the symbolic link creation.
- Correlate this event with other security alerts or logs to identify any patterns or additional suspicious activities involving the same user or system.

### False positive analysis

- Non-root users creating symbolic links for legitimate administrative tasks may trigger the rule. To manage this, identify and whitelist specific users or groups who regularly perform these tasks without malicious intent.
- Automated scripts or applications that use symbolic links for configuration management or software deployment might be flagged. Review these processes and exclude them by specifying the script or application names in the detection rule.
- Development environments where symbolic links are used to manage dependencies or version control can cause false positives. Exclude directories or processes associated with these environments to prevent unnecessary alerts.
- Backup or synchronization tools that create symbolic links as part of their operation may be mistakenly identified. Identify these tools and add exceptions for their typical execution patterns.
- System maintenance activities that involve symbolic link creation, such as linking to shared libraries or binaries, should be reviewed and excluded if they are part of routine operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or potential lateral movement by the attacker.
- Terminate any suspicious processes related to the 'ln' command that are identified in the alert to stop any ongoing malicious activity.
- Conduct a thorough review of the symbolic links created, especially those pointing to sensitive files or directories, and remove any unauthorized or suspicious links.
- Reset credentials and review access permissions for any accounts that may have been compromised or used in the attack, focusing on those with elevated privileges.
- Restore any altered or compromised files from a known good backup to ensure system integrity and prevent further exploitation.
- Implement additional monitoring and logging for symbolic link creation and other related activities to detect similar threats in the future.
- Escalate the incident to the security operations team for further investigation and to assess the need for broader organizational response measures.
