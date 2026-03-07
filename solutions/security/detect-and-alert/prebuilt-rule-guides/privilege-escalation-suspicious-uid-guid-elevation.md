---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Privilege Escalation via CAP_SETUID/SETGID Capabilities" prebuilt detection rule.
---

# Privilege Escalation via CAP_SETUID/SETGID Capabilities

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Privilege Escalation via CAP_SETUID/SETGID Capabilities

In Linux, CAP_SETUID and CAP_SETGID capabilities allow processes to change user and group IDs, crucial for identity management. Adversaries exploit misconfigurations to gain root access. The detection rule identifies processes with these capabilities that elevate privileges to root, excluding benign scenarios, to flag potential misuse.

### Possible investigation steps

- Review the process details such as process.name and process.executable to identify the specific application or script that triggered the alert. This can help determine if the process is expected or potentially malicious.
- Examine the process.parent.executable and process.parent.name fields to understand the parent process that initiated the suspicious process. This can provide context on whether the parent process is legitimate or part of a known attack vector.
- Check the user.id field to confirm the user context under which the process was executed. If the user is not expected to have elevated privileges, this could indicate a potential compromise.
- Investigate the process.command_line to analyze the command executed. Look for any unusual or unexpected command patterns that could suggest malicious intent.
- Correlate the alert with other security events or logs from the same host.id to identify any related suspicious activities or patterns that could indicate a broader attack.
- Assess the environment for any recent changes or misconfigurations that could have inadvertently granted CAP_SETUID or CAP_SETGID capabilities to unauthorized processes.

### False positive analysis

- Processes related to system management tools like VMware, SolarWinds, and language tools may trigger false positives. Exclude these by adding their executables to the exception list.
- Scheduled tasks or system updates that involve processes like update-notifier or dbus-daemon can cause false alerts. Consider excluding these parent process names from the detection rule.
- Automation tools such as Ansible or scripts executed by Python may inadvertently match the rule. Exclude command lines that match known automation patterns.
- Legitimate use of sudo or pkexec for administrative tasks can be misinterpreted as privilege escalation. Exclude these executables if they are part of regular administrative operations.
- Monitoring tools like osqueryd or saposcol might trigger the rule during normal operations. Add these process names to the exception list to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified with CAP_SETUID or CAP_SETGID capabilities that have escalated privileges to root, ensuring no further exploitation occurs.
- Conduct a thorough review of the affected system's user and group configurations to identify and correct any misconfigurations that allowed the privilege escalation.
- Revoke unnecessary CAP_SETUID and CAP_SETGID capabilities from processes and users that do not require them, reducing the attack surface for future exploitation.
- Restore the affected system from a known good backup if unauthorized changes or persistent threats are detected, ensuring the system is returned to a secure state.
- Monitor the system and network for any signs of continued or attempted exploitation, using enhanced logging and alerting to detect similar threats in the future.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
