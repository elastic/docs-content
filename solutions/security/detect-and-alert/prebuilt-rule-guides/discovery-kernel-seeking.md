---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kernel Seeking Activity" prebuilt detection rule.'
---

# Kernel Seeking Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kernel Seeking Activity

Kernel seeking involves probing the Linux kernel for symbols and functions, often using utilities like `tail`, `cmp`, `hexdump`, `xxd`, and `dd`. Adversaries exploit this to discover vulnerabilities for kernel exploitation. The detection rule identifies suspicious execution patterns of these utilities, particularly when accessing kernel-related paths, signaling potential malicious reconnaissance or exploitation attempts.

### Possible investigation steps

- Review the process execution details to confirm the use of utilities like `tail`, `cmp`, `hexdump`, `xxd`, or `dd` with the specified arguments, focusing on the `process.name` and `process.args` fields.
- Examine the `process.parent.args` and `process.args` fields to identify the specific kernel-related paths accessed, such as those under `/boot/*`, to understand the context of the access.
- Investigate the parent process of the suspicious activity by analyzing the `process.parent` field to determine if it was initiated by a legitimate or potentially malicious process.
- Check the timeline of events around the alert to identify any preceding or subsequent suspicious activities that might indicate a broader attack pattern.
- Correlate the alert with other security events or logs from the same host to assess if there are additional indicators of compromise or related malicious activities.
- Evaluate the user account associated with the process execution to determine if it aligns with expected behavior or if it might be compromised.

### False positive analysis

- System administrators or automated scripts may use utilities like `tail`, `cmp`, `hexdump`, `xxd`, and `dd` for legitimate maintenance tasks involving kernel files. To mitigate this, identify and whitelist specific scripts or processes that are known to perform these actions regularly.
- Backup or recovery operations might involve accessing kernel-related paths with these utilities. Exclude these operations by defining exceptions for known backup tools or processes that interact with the `/boot` directory.
- Developers working on kernel modules or custom kernel builds may trigger this rule during their normal workflow. Consider excluding specific user accounts or development environments from this rule to prevent false positives.
- Security tools or monitoring solutions that perform regular checks on kernel files could be mistakenly flagged. Review and whitelist these tools to ensure they are not incorrectly identified as threats.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, particularly those involving the utilities `tail`, `cmp`, `hexdump`, `xxd`, and `dd` accessing kernel paths.
- Conduct a thorough review of system logs and process execution history to identify any additional suspicious activities or related indicators of compromise.
- Restore the system from a known good backup if any unauthorized modifications to the kernel or system files are detected.
- Update the Linux kernel and all related packages to the latest versions to patch any known vulnerabilities that could be exploited.
- Implement enhanced monitoring and alerting for similar activities, focusing on the execution of the specified utilities with kernel-related arguments.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected.
