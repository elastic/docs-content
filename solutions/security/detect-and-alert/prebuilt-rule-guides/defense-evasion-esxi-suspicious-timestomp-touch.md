---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "ESXI Timestomping using Touch Command" prebuilt detection rule.'
---

# ESXI Timestomping using Touch Command

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating ESXI Timestomping using Touch Command

VMware ESXi is a hypervisor used to manage virtual machines. Adversaries may exploit the 'touch' command with the "-r" flag to alter file timestamps, masking unauthorized changes in VM-related directories. The detection rule identifies such activities by monitoring the execution of 'touch' with specific arguments, signaling potential timestamp tampering in critical VMware paths.

### Possible investigation steps

- Review the process execution details to confirm the presence of the 'touch' command with the "-r" flag and verify the specific VM-related paths involved, such as "/etc/vmware/", "/usr/lib/vmware/", or "/vmfs/*".
- Check the user account associated with the process execution to determine if it is a legitimate user or potentially compromised account.
- Investigate the parent process of the 'touch' command to understand the context of its execution and identify any related suspicious activities.
- Examine recent changes to the files in the specified paths to identify any unauthorized modifications or anomalies.
- Correlate the event with other security alerts or logs from the same host to identify patterns or additional indicators of compromise.
- Assess the system for any signs of unauthorized access or other defense evasion techniques that may have been employed by the threat actor.

### False positive analysis

- Routine administrative tasks in VMware environments may trigger the rule if administrators use the touch command with the -r flag for legitimate purposes. To manage this, create exceptions for known administrative scripts or processes that regularly perform these actions.
- Automated backup or synchronization tools that update file timestamps as part of their normal operation can cause false positives. Identify these tools and exclude their processes from the rule to prevent unnecessary alerts.
- System maintenance activities, such as updates or patches, might involve timestamp modifications in VMware directories. Coordinate with IT teams to whitelist these activities during scheduled maintenance windows.
- Custom scripts developed in-house for managing VMware environments might use the touch command with the -r flag. Review these scripts and, if verified as safe, add them to an exception list to avoid false positives.
- Security tools or monitoring solutions that perform integrity checks on VMware files may inadvertently alter timestamps. Ensure these tools are recognized and excluded from the rule to maintain accurate threat detection.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or tampering with VMware-related files.
- Conduct a thorough review of the affected system's logs and processes to identify any unauthorized changes or additional malicious activities.
- Restore the original timestamps of the affected files using verified backups to ensure the integrity of the VMware-related configurations.
- Revert any unauthorized changes to the VMware environment by restoring from a known good backup or snapshot.
- Update and patch the VMware ESXi and associated software to the latest versions to mitigate any known vulnerabilities that could be exploited.
- Implement stricter access controls and monitoring on critical VMware directories to prevent unauthorized modifications in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
