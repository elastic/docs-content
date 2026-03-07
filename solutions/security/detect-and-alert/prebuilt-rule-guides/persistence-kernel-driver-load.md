---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kernel Driver Load" prebuilt detection rule.
---

# Kernel Driver Load

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kernel Driver Load

Kernel modules extend the functionality of the Linux kernel, allowing dynamic loading of drivers and other components. Adversaries exploit this by loading malicious modules, or rootkits, to gain stealthy control over systems. The 'Kernel Driver Load' detection rule leverages auditd to monitor system calls like `init_module`, identifying unauthorized module loads indicative of potential rootkit activity, thus enhancing threat detection and system integrity.

### Possible investigation steps

- Review the alert details to identify the specific host where the kernel module was loaded, focusing on the host.os.type field to confirm it is a Linux system.
- Examine the event.action field to verify that the action was indeed "loaded-kernel-module" and check the auditd.data.syscall field for the specific system call used, either "init_module" or "finit_module".
- Investigate the timeline of events on the affected host around the time of the alert to identify any suspicious activities or changes, such as new user accounts, unexpected network connections, or file modifications.
- Check the system logs and audit logs on the affected host for any additional context or anomalies that coincide with the module load event.
- Identify the source and legitimacy of the loaded kernel module by examining the module's file path, signature, and associated metadata, if available.
- Assess the potential impact and scope of the incident by determining if similar alerts have been triggered on other hosts within the environment, indicating a broader campaign or attack.

### False positive analysis

- Legitimate kernel module updates or installations can trigger alerts. Regularly scheduled updates or installations by trusted administrators should be documented and excluded from monitoring to reduce noise.
- System utilities that load kernel modules as part of their normal operation may cause false positives. Identify these utilities and create exceptions for their expected behavior.
- Automated configuration management tools that deploy or update kernel modules can generate alerts. Ensure these tools are recognized and their activities are whitelisted.
- Development environments where kernel modules are frequently compiled and tested may lead to frequent alerts. Exclude specific development hosts or processes from monitoring to avoid unnecessary alerts.
- Security software that loads kernel modules for protection purposes might be flagged. Verify and exclude these modules if they are from trusted vendors.

### Response and remediation

- Isolate the affected system from the network immediately to prevent further malicious activity and lateral movement.
- Verify the legitimacy of the loaded kernel module by checking its source and integrity. If the module is unauthorized or suspicious, unload it using appropriate system commands.
- Conduct a thorough scan of the system using updated antivirus or anti-malware tools to identify and remove any additional malicious components or rootkits.
- Review and analyze system logs, especially those related to auditd, to identify any unauthorized access or changes made by the adversary. This can help in understanding the scope of the compromise.
- Restore the system from a known good backup if the integrity of the system is in question and if the malicious activity cannot be fully remediated.
- Implement stricter access controls and monitoring on kernel module loading activities to prevent unauthorized actions in the future. This may include restricting module loading to trusted users or processes.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
