---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Boot File Copy" prebuilt detection rule.'
---

# Boot File Copy

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Boot File Copy
The `/boot` directory in Linux systems is crucial for storing files necessary for booting, such as the kernel. Adversaries may exploit this by copying or moving files to alter the boot process, potentially gaining persistent access. The 'Boot File Copy' detection rule identifies suspicious file operations in this directory, excluding legitimate processes, to flag potential unauthorized modifications.

### Possible investigation steps

- Review the process details to identify the specific file operation by examining the process name and arguments, particularly focusing on the use of 'cp' or 'mv' commands with paths involving '/boot/*'.
- Investigate the parent process executable and name to determine if the operation was initiated by a known legitimate process or script, ensuring it is not one of the excluded processes like 'update-initramfs' or 'grub-mkconfig'.
- Check the user account associated with the process to assess whether it is a privileged account and if the activity aligns with typical user behavior.
- Analyze recent system logs and audit records for any other suspicious activities or anomalies around the time of the alert to identify potential patterns or related events.
- Verify the integrity and authenticity of the files in the /boot directory to ensure no unauthorized modifications have been made, focusing on critical files like the kernel and initramfs images.
- If possible, correlate the alert with other data sources such as Elastic Endgame or Crowdstrike to gather additional context and confirm whether this is part of a broader attack pattern.

### False positive analysis

- System updates and maintenance tasks often involve legitimate processes that interact with the /boot directory. Processes like update-initramfs, dracut, and grub-mkconfig are common during these operations. Users can exclude these processes by adding them to the exception list in the detection rule.
- Custom scripts or administrative tasks that require copying or moving files to the /boot directory may trigger false positives. Identify these scripts and add their parent process names or paths to the exclusion criteria.
- Package management operations, such as those involving dpkg or rpm, may also interact with the /boot directory. Exclude paths like /var/lib/dpkg/info/* and /var/tmp/rpm-tmp.* to prevent these from being flagged.
- Temporary system recovery or installation processes might use directories like /tmp/newroot. Exclude these paths to avoid unnecessary alerts during legitimate recovery operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or potential lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule, specifically those involving unauthorized 'cp' or 'mv' operations in the /boot directory.
- Conduct a thorough review of the /boot directory to identify and remove any unauthorized files or modifications. Restore any altered files from a known good backup if necessary.
- Check for any unauthorized changes to boot configuration files, such as GRUB or LILO, and restore them to their original state.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement additional monitoring on the affected system and similar systems to detect any further unauthorized access attempts or modifications.
- Review and update access controls and permissions for the /boot directory to ensure only authorized processes and users can make changes.
