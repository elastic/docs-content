---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Kernel Module Enumeration" prebuilt detection rule.'
---

# Unusual Kernel Module Enumeration

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Kernel Module Enumeration

Loadable Kernel Modules (LKMs) enhance a Linux kernel's capabilities dynamically, without requiring a system reboot. Adversaries may exploit this by enumerating kernel modules to gather system information or identify vulnerabilities. The detection rule identifies suspicious enumeration activities by monitoring specific processes and arguments associated with module listing commands, while excluding benign parent processes to reduce false positives.

### Possible investigation steps

- Review the process details in the alert to identify the specific command used for kernel module enumeration, such as lsmod, modinfo, kmod with list argument, or depmod with --all or -a arguments.
- Examine the process parent name to ensure it is not one of the benign processes listed in the exclusion criteria, such as mkinitramfs, dracut, or systemd, which could indicate a false positive.
- Investigate the user account associated with the process to determine if the activity aligns with expected behavior or if it might indicate unauthorized access.
- Check the timing and frequency of the enumeration activity to assess whether it is part of routine system operations or an anomaly that warrants further investigation.
- Correlate the alert with other security events or logs from the same host to identify any additional suspicious activities or patterns that could suggest a broader attack or compromise.

### False positive analysis

- System maintenance tools like mkinitramfs and dracut may trigger the rule during legitimate operations. To handle this, ensure these processes are included in the exclusion list to prevent unnecessary alerts.
- Backup and recovery processes such as rear and casper can cause false positives when they interact with kernel modules. Verify these processes are part of the exclusion criteria to avoid misidentification.
- Disk management and storage tools like lvm2 and mdadm might enumerate kernel modules as part of their normal function. Add these to the exclusion list to reduce false positives.
- Virtualization and container management tools such as vz-start and overlayroot may also enumerate modules. Confirm these are excluded to maintain focus on genuine threats.
- Kernel update and management utilities like dkms and kernel-install can trigger alerts during updates. Ensure these are accounted for in the exclusion list to minimize false alarms.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule, specifically those involving unauthorized use of lsmod, modinfo, kmod, or depmod commands.
- Conduct a thorough review of recent system logs and process execution history to identify any unauthorized access or changes made to the system.
- Restore the system from a known good backup if any unauthorized modifications to kernel modules or system files are detected.
- Update and patch the system to the latest security standards to mitigate any known vulnerabilities that could be exploited through kernel modules.
- Implement stricter access controls and monitoring for kernel module management, ensuring only authorized personnel can load or unload modules.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
