---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Path Invocation from Command Line" prebuilt detection rule.
---

# Suspicious Path Invocation from Command Line

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Path Invocation from Command Line

In Linux environments, shell processes like bash or zsh execute commands, often using the PATH variable to locate executables. Adversaries may manipulate PATH to run malicious scripts from non-standard directories, evading detection. The detection rule identifies unusual PATH assignments in command lines, signaling potential unauthorized actions by monitoring specific shell invocations and command patterns.

### Possible investigation steps

- Review the command line details captured in the alert to identify the specific PATH assignment and the command being executed. This can provide insight into whether the command is expected or potentially malicious.
- Check the process tree to understand the parent process and any child processes spawned by the suspicious shell invocation. This can help determine the context in which the command was executed.
- Investigate the user account associated with the process to determine if the activity aligns with the user's typical behavior or if the account may have been compromised.
- Examine the directory from which the command is being executed to verify if it is a non-standard or suspicious location. Look for any unusual files or scripts in that directory.
- Cross-reference the event with other security logs or alerts to identify any correlated activities that might indicate a broader attack or compromise.
- Assess the system's recent changes or updates to determine if they could have inadvertently caused the PATH modification or if it was intentionally altered by an adversary.

### False positive analysis

- System administrators or developers may intentionally modify the PATH variable for legitimate purposes, such as testing scripts or applications in development environments. To handle this, create exceptions for known users or specific directories commonly used for development.
- Automated scripts or configuration management tools might alter the PATH variable as part of their normal operation. Identify these scripts and exclude their execution paths or user accounts from triggering alerts.
- Some software installations or updates may temporarily change the PATH variable to include non-standard directories. Monitor installation processes and whitelist these activities when performed by trusted sources.
- Custom shell configurations or user profiles might include PATH modifications for convenience or performance reasons. Review and document these configurations, and exclude them from detection if they are verified as non-threatening.
- Educational or training environments where users experiment with shell commands may frequently trigger this rule. Consider excluding specific user groups or environments dedicated to learning and experimentation.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement or data exfiltration.
- Terminate any suspicious processes identified by the alert to stop any ongoing unauthorized actions.
- Review the command history and PATH variable changes on the affected system to identify any unauthorized modifications or scripts executed from non-standard directories.
- Restore the PATH variable to its default state to ensure that only trusted directories are used for command execution.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection tools to identify and remove any malicious scripts or files.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
- Implement monitoring for similar PATH manipulation attempts across the network to enhance detection and prevent recurrence.
