---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Chroot Container Escape via Mount" prebuilt detection rule.'
---

# Potential Chroot Container Escape via Mount

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Chroot Container Escape via Mount

Chroot and mount are Linux utilities that can isolate processes and manage file systems, respectively. Adversaries may exploit these to escape containerized environments by mounting the host's root file system and using chroot to change the root directory, gaining unauthorized access. The detection rule identifies this rare sequence by monitoring for mount and chroot executions within a short timeframe, signaling potential privilege escalation attempts.

### Possible investigation steps

- Review the alert details to identify the specific host.id and process.parent.entity_id associated with the alert to understand which system and parent process are involved.
- Examine the process execution timeline to confirm the sequence of the mount and chroot commands, ensuring they occurred within the specified maxspan of 5 minutes.
- Investigate the process.args field for the mount command to determine the specific device or file system being targeted, especially focusing on any /dev/sd* entries that suggest attempts to access physical disks.
- Check the user permissions and roles associated with the process.parent.name (e.g., bash, dash, sh) to assess if the user had sufficient privileges to perform such operations.
- Analyze the broader context of the host.os.type to identify any recent changes or anomalies in the Linux environment that could have facilitated this behavior.
- Correlate with other security logs or alerts from the same host to identify any additional suspicious activities or patterns that might indicate a broader attack or compromise.

### False positive analysis

- System maintenance scripts may trigger the rule if they involve mounting and chroot operations. Review scheduled tasks and scripts to identify legitimate use and consider excluding these specific processes from the rule.
- Backup or recovery operations that require mounting file systems and changing root directories can also cause false positives. Identify these operations and create exceptions for the associated processes or users.
- Development or testing environments where users frequently perform mount and chroot operations for legitimate purposes may trigger alerts. Evaluate the necessity of these actions and exclude known safe processes or users.
- Automated deployment tools that use mount and chroot as part of their setup routines can be mistaken for malicious activity. Verify the tools and their processes, then add them to an exclusion list if they are deemed safe.
- Custom scripts executed by trusted users that involve mount and chroot should be reviewed. If these scripts are part of regular operations, consider excluding them from the detection rule.

### Response and remediation

- Immediately isolate the affected container to prevent further unauthorized access or potential lateral movement within the host system.
- Terminate any suspicious processes identified as executing the mount or chroot commands within the container to halt any ongoing escape attempts.
- Conduct a thorough review of the container's permissions and configurations to ensure that only necessary privileges are granted, reducing the risk of similar exploits.
- Inspect the host system for any signs of compromise or unauthorized access, focusing on logs and system changes around the time of the detected activity.
- Restore the container from a known good backup if any unauthorized changes or compromises are detected, ensuring the environment is clean and secure.
- Update and patch the container and host systems to address any known vulnerabilities that could be exploited for privilege escalation or container escape.
- Escalate the incident to the security operations team for further analysis and to determine if additional monitoring or security measures are required to prevent future occurrences.
