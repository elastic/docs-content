---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Git Hook Command Execution" prebuilt detection rule.'
---

# Git Hook Command Execution

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Git Hook Command Execution

Git hooks are scripts that automate tasks by executing before or after Git events like commits or pushes. While useful for developers, adversaries can exploit them to run malicious commands, gaining persistence or evading defenses. The detection rule identifies suspicious processes initiated by Git hooks, focusing on shell executions, to flag potential abuse on Linux systems.

### Possible investigation steps

- Review the alert details to identify the specific Git hook script path and the suspicious process name that was executed, as indicated by the process.args and process.name fields.
- Examine the process tree to understand the parent-child relationship, focusing on the process.parent.name and process.entity_id fields, to determine how the suspicious process was initiated.
- Check the Git repository's history and recent changes to the .git/hooks directory to identify any unauthorized modifications or additions to the hook scripts.
- Investigate the user account associated with the process execution to determine if the activity aligns with their typical behavior or if it indicates potential compromise.
- Analyze the command-line arguments and environment variables of the suspicious process to gather more context on the nature of the executed command.
- Correlate this event with other security alerts or logs from the same host.id to identify any patterns or additional indicators of compromise.
- If possible, isolate the affected system and conduct a deeper forensic analysis to uncover any further malicious activity or persistence mechanisms.

### False positive analysis

- Developers using Git hooks for legitimate automation tasks may trigger this rule. To manage this, identify and document common scripts used in your development environment and create exceptions for these known benign processes.
- Continuous integration and deployment (CI/CD) systems often utilize Git hooks to automate workflows. Review the processes initiated by these systems and exclude them from detection if they are verified as non-malicious.
- Custom scripts executed via Git hooks for project-specific tasks can also cause false positives. Collaborate with development teams to catalog these scripts and adjust the detection rule to exclude them.
- Frequent updates or changes in Git repositories might lead to repeated triggering of the rule. Monitor these activities and, if consistent and verified as safe, consider adding them to an allowlist to reduce noise.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes identified as being executed from Git hooks, especially those involving shell executions.
- Conduct a thorough review of the .git/hooks directory on the affected system to identify and remove any unauthorized or malicious scripts.
- Restore any modified or deleted files from a known good backup to ensure system integrity.
- Implement monitoring for any future modifications to the .git/hooks directory to detect unauthorized changes promptly.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Review and update access controls and permissions for Git repositories to limit the ability to modify hooks to trusted users only.
