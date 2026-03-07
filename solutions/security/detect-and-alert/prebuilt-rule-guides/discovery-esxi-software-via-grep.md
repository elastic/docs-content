---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "ESXI Discovery via Grep" prebuilt detection rule.'
---

# ESXI Discovery via Grep

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating ESXI Discovery via Grep

In Linux environments, tools like 'grep' are used to search through files for specific patterns. Adversaries may exploit these tools to locate and analyze virtual machine files, which are crucial for ESXi environments. The detection rule identifies suspicious use of 'grep' variants targeting VM file extensions, signaling potential reconnaissance or manipulation attempts by threat actors. This rule helps in early detection of such malicious activities by monitoring process execution patterns.

### Possible investigation steps

- Review the process execution details to confirm the presence of 'grep', 'egrep', or 'pgrep' with arguments related to VM file extensions such as "vmdk", "vmx", "vmxf", "vmsd", "vmsn", "vswp", "vmss", "nvram", or "vmem".
- Check the parent process of the suspicious 'grep' command to determine if it is a legitimate process or potentially malicious, ensuring it is not "/usr/share/qemu/init/qemu-kvm-init".
- Investigate the user account associated with the process execution to assess if the activity aligns with their typical behavior or if it appears anomalous.
- Examine recent system logs and other security alerts for additional indicators of compromise or related suspicious activities on the host.
- Assess the network activity from the host to identify any unusual connections or data exfiltration attempts that may correlate with the discovery activity.

### False positive analysis

- System administrators or automated scripts may use grep to search for VM-related files as part of routine maintenance or monitoring tasks. To handle this, create exceptions for known administrative scripts or processes by excluding specific parent processes or user accounts.
- Backup or snapshot management tools might invoke grep to verify the presence of VM files. Identify these tools and exclude their process names or paths from the detection rule to prevent false alerts.
- Developers or IT staff conducting legitimate audits or inventory checks on VM files may trigger this rule. Consider excluding specific user accounts or groups that are authorized to perform such activities.
- Security tools or monitoring solutions that perform regular checks on VM files could also cause false positives. Whitelist these tools by excluding their executable paths or process names from the rule.

### Response and remediation

- Isolate the affected Linux system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, specifically those involving 'grep', 'egrep', or 'pgrep' with VM-related file extensions.
- Conduct a thorough review of the system's recent process execution history and file access logs to identify any unauthorized access or changes to VM files.
- Restore any compromised or altered VM files from a known good backup to ensure system integrity and continuity.
- Implement stricter access controls and permissions on VM-related files to limit exposure to unauthorized users or processes.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Update and enhance monitoring rules to detect similar patterns of suspicious activity, ensuring early detection of future threats.
