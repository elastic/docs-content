---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "File made Immutable by Chattr" prebuilt detection rule.
---

# File made Immutable by Chattr

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating File made Immutable by Chattr

The `chattr` command in Linux is used to change file attributes, including making files immutable, which prevents modifications or deletions. Adversaries exploit this to secure malicious files or altered system files against tampering, aiding persistence. The detection rule identifies suspicious use of `chattr` by monitoring process executions, filtering out benign parent processes, and focusing on those altering immutability attributes, thus highlighting potential misuse.

### Possible investigation steps

- Review the process execution details to confirm the use of the chattr command with arguments altering immutability, specifically looking for "+i" or "-i" in process.args.
- Identify the file(s) targeted by the chattr command to determine if they are critical system files or files commonly targeted by threat actors, such as .ssh or /etc/passwd.
- Investigate the parent process of the chattr execution by examining process.parent.executable and process.parent.name to determine if it is a known benign process or potentially malicious.
- Check the user context under which the chattr command was executed to assess if it aligns with expected administrative activity or if it indicates unauthorized access.
- Correlate the event with other security alerts or logs to identify any related suspicious activities, such as unauthorized access attempts or changes to other system files.
- Evaluate the risk and impact of the immutable file(s) on system operations and security posture, considering the potential for persistence or defense evasion by threat actors.

### False positive analysis

- System processes like systemd and cf-agent may invoke chattr for legitimate reasons, such as system maintenance or configuration management. To handle these, exclude these processes by adding them to the exception list in the detection rule.
- Scheduled tasks or scripts that use chattr to manage file attributes for security or operational purposes can trigger false positives. Identify these tasks and exclude their parent processes from the rule.
- Administrative actions performed by authorized users, such as securing configuration files, might be flagged. Regularly review and update the list of known benign parent processes to prevent unnecessary alerts.
- Security tools or agents that modify file attributes as part of their protection mechanisms can cause false positives. Ensure these tools are recognized and excluded by their executable paths or parent process names.

### Response and remediation

- Isolate the affected system from the network to prevent further spread or communication with potential command and control servers.
- Identify and terminate any malicious processes associated with the `chattr` command to stop further unauthorized file modifications.
- Restore the affected files from a known good backup, ensuring that any immutable attributes set by the attacker are removed.
- Conduct a thorough review of user accounts and permissions on the affected system to ensure no unauthorized access or privilege escalation has occurred.
- Implement file integrity monitoring to detect unauthorized changes to critical system files, enhancing detection capabilities for similar threats.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are compromised.
- Review and update security policies and configurations to prevent unauthorized use of the `chattr` command, such as restricting its execution to trusted administrators only.
