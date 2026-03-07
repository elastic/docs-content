---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kernel Object File Creation" prebuilt detection rule.'
---

# Kernel Object File Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kernel Object File Creation

Kernel object files (.ko) are loadable modules that extend the functionality of the Linux kernel, often used for adding drivers or system features. Adversaries exploit this by loading malicious modules, such as rootkits, to gain control and evade detection. The detection rule identifies suspicious .ko file creation, excluding benign paths, to flag potential threats while minimizing false positives.

### Possible investigation steps

- Review the file path of the created .ko file to determine if it is located in a suspicious or unusual directory that is not excluded by the rule, such as /var/tmp or /usr/local.
- Examine the process that created the .ko file by checking the process.executable and process.name fields to identify if it is a known legitimate process or potentially malicious.
- Investigate the parent process of the process that created the .ko file to understand the context of how the file was created and if it was initiated by a legitimate user action or a script.
- Check for any recent system changes or anomalies around the time of the .ko file creation, such as new user accounts, changes in system configurations, or other suspicious file activities.
- Look for any associated network activity from the host around the time of the .ko file creation to identify potential command and control communications or data exfiltration attempts.
- Correlate the alert with other security events or logs from the same host to identify any patterns or additional indicators of compromise that may suggest a broader attack campaign.

### False positive analysis

- Kernel updates and system maintenance activities can generate .ko files in legitimate scenarios. Users should monitor for these activities and consider excluding paths related to official update processes.
- Custom kernel module development by developers or system administrators may trigger this rule. Establish a process to whitelist known development environments or specific user accounts involved in module creation.
- Automated system recovery tools, such as those using mkinitramfs, may create .ko files. Ensure these paths are excluded as indicated in the rule to prevent unnecessary alerts.
- Snap package installations might involve .ko file creation. Exclude the /snap/ directory to avoid false positives from legitimate package installations.
- Backup and restoration processes using tools like cpio can lead to .ko file creation. Verify these processes and exclude them if they are part of routine system operations.

### Response and remediation

- Isolate the affected system from the network to prevent further spread or communication with potential command and control servers.
- Terminate any suspicious processes associated with the creation of the .ko file, especially those not originating from known benign paths.
- Remove the suspicious .ko file from the system to prevent it from being loaded into the kernel.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious components.
- Review system logs and audit trails to identify any unauthorized access or changes made around the time of the .ko file creation.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the threat is part of a larger attack campaign.
- Implement additional monitoring and alerting for similar activities, ensuring that any future attempts to create or load unauthorized .ko files are promptly detected and addressed.
