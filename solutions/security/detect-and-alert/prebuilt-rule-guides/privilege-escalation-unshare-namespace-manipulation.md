---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Namespace Manipulation Using Unshare" prebuilt detection rule.
---

# Namespace Manipulation Using Unshare

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Namespace Manipulation Using Unshare

The `unshare` command in Linux is used to create new namespaces, isolating processes from the rest of the system. This isolation is crucial for containerization and security. However, attackers can exploit `unshare` to break out of containers or elevate privileges by creating namespaces that bypass security controls. The detection rule identifies suspicious `unshare` executions by monitoring process starts, filtering out benign parent processes, and focusing on unusual usage patterns, thus highlighting potential misuse.

### Possible investigation steps

- Review the process tree to understand the context of the unshare execution, focusing on the parent process and any child processes spawned by unshare.
- Investigate the user account associated with the unshare execution to determine if it is a legitimate user or potentially compromised.
- Examine the command-line arguments used with unshare to identify any unusual or suspicious options that may indicate an attempt to bypass security controls.
- Check for any recent changes or anomalies in the system logs around the time of the unshare execution to identify potential indicators of compromise or privilege escalation attempts.
- Correlate the unshare event with other security alerts or logs to determine if it is part of a larger attack pattern or campaign.

### False positive analysis

- System management tools like udevadm and systemd-udevd may invoke unshare as part of their normal operations. These should be excluded by ensuring the rule filters out processes with these as parent executables.
- Snap package management can trigger unshare during its operations. Exclude processes where the arguments include /usr/bin/snap to prevent unnecessary alerts.
- Java applications might occasionally use unshare for legitimate purposes. Exclude processes with java as the parent name to reduce false positives.
- Custom scripts or administrative tasks that use unshare for legitimate namespace management should be reviewed and, if deemed safe, added to the exclusion list to prevent repeated alerts.

### Response and remediation

- Immediately isolate the affected system to prevent further unauthorized access or lateral movement within the network.
- Terminate any suspicious processes associated with the `unshare` command that do not have legitimate parent processes or arguments, as identified in the detection query.
- Conduct a thorough review of system logs and process trees to identify any additional unauthorized or suspicious activities that may have occurred in conjunction with the `unshare` execution.
- Revoke any unauthorized access or privileges that may have been granted as a result of the namespace manipulation, ensuring that all user and process permissions are appropriately restricted.
- Restore the affected system from a known good backup if any unauthorized changes or damage to the system integrity are detected.
- Implement additional monitoring and alerting for unusual `unshare` usage patterns to enhance detection capabilities and prevent future occurrences.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems or data have been compromised.
