---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Initramfs Unpacking via unmkinitramfs" prebuilt detection rule.
---

# Initramfs Unpacking via unmkinitramfs

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Initramfs Unpacking via unmkinitramfs

Initramfs is a crucial component in Linux boot processes, containing essential drivers and scripts. The `unmkinitramfs` tool extracts its contents, which attackers might exploit to insert malicious code, ensuring persistence. The detection rule identifies the execution of `unmkinitramfs`, flagging potential unauthorized modifications by monitoring process initiation events on Linux systems.

### Possible investigation steps

- Review the process execution details to confirm the presence of the unmkinitramfs command, focusing on the process.name field to ensure it matches "unmkinitramfs".
- Check the user context under which the unmkinitramfs command was executed to determine if it aligns with expected administrative activities or if it was run by an unauthorized user.
- Investigate the parent process of the unmkinitramfs execution to understand how the command was initiated and if it was part of a legitimate script or an unexpected process chain.
- Examine recent system logs and audit logs for any other suspicious activities or anomalies around the time of the unmkinitramfs execution, such as unauthorized access attempts or changes to critical system files.
- Assess the integrity of the initramfs image by comparing it with a known good version, if available, to identify any unauthorized modifications or inclusions of malicious code.

### False positive analysis

- Routine system maintenance or updates may trigger the rule when legitimate processes unpack initramfs for kernel updates. Users can create exceptions for known maintenance scripts or processes that regularly perform these actions.
- Automated backup or recovery solutions might use unmkinitramfs to verify or restore system images. Identify and exclude these processes if they are part of trusted backup operations.
- Developers or system administrators testing or customizing initramfs images for legitimate purposes could trigger the rule. Establish a whitelist for specific user accounts or scripts that are authorized to perform these tasks.
- Security tools or monitoring solutions that analyze initramfs contents for integrity checks might inadvertently trigger the rule. Ensure these tools are recognized and excluded from detection to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement or data exfiltration by the attacker.
- Terminate any suspicious processes related to `unmkinitramfs` to halt any ongoing malicious activity.
- Conduct a thorough review of the initramfs image and its contents to identify and remove any unauthorized modifications or malicious code.
- Restore the initramfs image from a known good backup to ensure system integrity and remove any potential backdoors.
- Monitor the system for any further attempts to execute `unmkinitramfs` and investigate any such occurrences to determine if they are legitimate or part of an ongoing attack.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems may be affected.
- Implement additional logging and monitoring for process execution events on Linux systems to enhance detection capabilities for similar threats in the future.
