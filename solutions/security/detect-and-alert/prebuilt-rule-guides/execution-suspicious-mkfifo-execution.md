---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Named Pipe Creation" prebuilt detection rule.
---

# Suspicious Named Pipe Creation

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Named Pipe Creation

Named pipes, or FIFOs, are a form of inter-process communication in Linux environments, allowing data transfer between processes. Adversaries exploit this by creating named pipes in common directories like /tmp to stealthily execute commands or maintain persistence. The detection rule identifies unusual named pipe creation by monitoring the `mkfifo` command, especially when initiated by common shell processes, to flag potential malicious activity.

### Possible investigation steps

- Review the process command line arguments to identify the exact named pipe path and any associated commands or scripts that might have been executed using the named pipe.
- Investigate the parent process (bash, csh, dash, fish, ksh, sh, tcsh, or zsh) to determine the origin of the mkfifo command, checking for any unusual or unexpected scripts or commands that might have initiated it.
- Examine the user account associated with the mkfifo process to determine if it is a legitimate user or if the account might have been compromised.
- Check for any other suspicious activities or processes running under the same user account or originating from the same parent process to identify potential lateral movement or further malicious actions.
- Analyze the system logs around the time of the named pipe creation for any other indicators of compromise, such as unauthorized access attempts or unusual network connections.
- If possible, capture and review the contents of the named pipe to understand the data being transferred and assess whether it is part of a malicious operation.

### False positive analysis

- Named pipes created by legitimate applications for inter-process communication can trigger this rule. Users should identify and whitelist these applications by adding exceptions for specific process command lines that are known to be safe.
- System maintenance scripts or backup processes that use named pipes in directories like /tmp or /var/tmp may cause false positives. Review these scripts and exclude them from the rule if they are verified as non-malicious.
- Development environments or testing frameworks that frequently create and delete named pipes during their operations might be flagged. Users can mitigate this by excluding these environments from monitoring or by specifying exceptions for known development tools.
- Automated deployment tools that use named pipes for configuration management or orchestration tasks can also be a source of false positives. Ensure these tools are recognized and excluded from the rule to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity or lateral movement.
- Terminate any suspicious processes associated with the mkfifo command, especially those originating from common shell processes like bash or sh.
- Delete any named pipes created in directories such as /tmp, /dev/shm, or /var/tmp that do not follow expected naming conventions or are not part of legitimate applications.
- Conduct a thorough review of user accounts and permissions on the affected system to identify any unauthorized access or privilege escalation.
- Restore the system from a known good backup if any unauthorized changes or persistence mechanisms are detected.
- Implement additional monitoring on the affected system and network to detect any further attempts to create suspicious named pipes or execute unauthorized commands.
- Escalate the incident to the security operations team for further investigation and to determine if the threat is part of a larger attack campaign.

