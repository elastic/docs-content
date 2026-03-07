---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Initramfs Extraction via CPIO" prebuilt detection rule.
---

# Initramfs Extraction via CPIO

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Initramfs Extraction via CPIO

Initramfs is a temporary filesystem used during the Linux boot process, containing essential drivers and scripts. Attackers may exploit the `cpio` command to extract and modify initramfs, embedding malicious files to ensure persistence. The detection rule identifies suspicious `cpio` usage by monitoring process execution patterns, excluding legitimate parent processes, to flag potential threats.

### Possible investigation steps

- Review the process execution details to confirm the presence of the cpio command with arguments "-H" or "--format" and "newc" to ensure the alert is not a false positive.
- Investigate the parent process of the cpio command to determine if it is an unexpected or unauthorized process, as legitimate processes like mkinitramfs or dracut should be excluded.
- Check the execution path of the parent process to verify if it matches any known legitimate paths such as "/usr/share/initramfs-tools/*" or "/nix/store/*".
- Analyze the timeline of events around the cpio execution to identify any preceding or subsequent suspicious activities that might indicate a broader attack or persistence mechanism.
- Examine the system for any unauthorized modifications or additions to the initramfs image that could indicate tampering or the presence of malicious files.
- Correlate the alert with other security data sources like Elastic Endgame, Elastic Defend, or Crowdstrike to gather additional context and assess the scope of the potential threat.

### False positive analysis

- Legitimate system updates or maintenance activities may trigger the rule when tools like mkinitramfs or dracut are used. To handle this, ensure these processes are excluded by verifying that the parent process is mkinitramfs or dracut.
- Custom scripts or automation tools that manage initramfs might use cpio in a non-malicious context. Review these scripts and add their parent process names or paths to the exclusion list if they are verified as safe.
- Systems using non-standard initramfs management tools located in directories like /usr/share/initramfs-tools or /nix/store may cause false positives. Confirm these tools' legitimacy and update the exclusion paths accordingly.
- Development or testing environments where initramfs is frequently modified for legitimate reasons can generate alerts. Consider creating environment-specific exceptions to reduce noise while maintaining security in production systems.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or spread of potential malware.
- Terminate any suspicious processes related to the `cpio` command that do not have legitimate parent processes, such as `mkinitramfs` or `dracut`.
- Conduct a thorough review of the extracted initramfs contents to identify and remove any unauthorized or malicious files.
- Restore the initramfs from a known good backup to ensure system integrity and remove any potential persistence mechanisms.
- Monitor the system for any further suspicious activity, particularly related to the `cpio` command, to ensure the threat has been fully mitigated.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems may be affected.
- Update security policies and procedures to include specific checks for unauthorized `cpio` usage and enhance detection capabilities for similar threats.
