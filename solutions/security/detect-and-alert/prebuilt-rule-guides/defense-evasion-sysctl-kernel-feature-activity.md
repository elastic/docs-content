---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Kernel Feature Activity" prebuilt detection rule.
---

# Suspicious Kernel Feature Activity

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Kernel Feature Activity

Kernel features in Linux systems are critical for maintaining security and stability. They control various system behaviors, such as memory randomization and process tracing. Adversaries may exploit these features to weaken defenses, for instance, by disabling address space layout randomization (ASLR) or enabling unrestricted process tracing. The detection rule identifies suspicious activities by monitoring command executions that modify or read kernel settings, focusing on unusual patterns or contexts that suggest malicious intent.

### Possible investigation steps

- Review the process command line to identify which specific kernel feature was accessed or modified, focusing on entries like kernel.randomize_va_space or kernel.yama.ptrace_scope.
- Examine the parent process executable and name to determine the context in which the suspicious command was executed, checking for unusual or unauthorized parent processes.
- Investigate the user account associated with the process execution to assess whether the activity aligns with expected behavior for that user.
- Check for any recent changes in the /etc/sysctl.conf or /etc/sysctl.d/ directories that might indicate unauthorized modifications to kernel settings.
- Analyze the system's process execution history to identify any patterns or sequences of commands that suggest a broader attack or compromise.
- Correlate the alert with other security events or logs to determine if this activity is part of a larger attack campaign or isolated incident.

### False positive analysis

- System administrators or automated scripts may frequently modify kernel settings for legitimate purposes such as performance tuning or system maintenance. To handle these, identify and whitelist known administrative scripts or processes that regularly perform these actions.
- Security tools or monitoring solutions might execute commands that read kernel settings as part of their normal operation. Review and exclude these tools from triggering alerts by adding them to an exception list based on their process names or command patterns.
- Developers and testers might disable certain kernel features temporarily during debugging or testing phases. Coordinate with development teams to document these activities and exclude them from detection by specifying the relevant process names or command lines.
- Some system management tools may use commands like sysctl to apply configuration changes across multiple systems. If these tools are verified as non-threatening, exclude their specific command patterns or parent processes from triggering the rule.
- Regular system updates or configuration management processes might involve reading or modifying kernel settings. Identify these processes and add them to an exception list to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further exploitation or lateral movement by the adversary.
- Review and revert any unauthorized changes to kernel settings, such as ASLR, ptrace scope, or NMI watchdog, to their secure defaults using sysctl or by editing configuration files.
- Conduct a thorough examination of the system for signs of compromise, including checking for unauthorized access, unusual processes, or modifications to critical files.
- Restore the system from a known good backup if the integrity of the system is compromised and cannot be reliably remediated.
- Implement additional monitoring and logging for kernel feature modifications to detect similar activities in the future, ensuring alerts are configured for immediate response.
- Escalate the incident to the security operations center (SOC) or relevant security team for further investigation and correlation with other potential threats across the network.
- Review and update security policies and configurations to prevent unauthorized kernel modifications, including enforcing stricter access controls and auditing procedures.

