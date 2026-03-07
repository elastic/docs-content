---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Path Mounted" prebuilt detection rule.
---

# Suspicious Path Mounted

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Path Mounted

In Linux environments, the mount command integrates filesystems, enabling access to storage devices. Adversaries exploit this by mounting malicious filesystems in sensitive directories like /tmp or /dev/shm to exfiltrate data or maintain persistence. The detection rule identifies such activities by monitoring the execution of the mount command in unusual paths, excluding legitimate parent processes, thus highlighting potential threats.

### Possible investigation steps

- Review the process details to confirm the execution of the mount command, focusing on the process.name and process.args fields to identify the specific path being mounted.
- Examine the process.parent.executable field to determine the parent process that initiated the mount command, ensuring it is not a known legitimate process.
- Investigate the user account associated with the process to determine if it is a privileged account or if there are any signs of compromise.
- Check for any recent changes or anomalies in the mounted directories, such as unexpected files or modifications, to assess potential data exfiltration or persistence activities.
- Correlate the event with other security alerts or logs from the same host to identify any related suspicious activities or patterns that could indicate a broader attack.

### False positive analysis

- System maintenance scripts may trigger the rule if they mount filesystems in monitored paths. Review and whitelist these scripts by adding their parent executable paths to the exclusion list.
- Backup processes that temporarily mount directories for data transfer can be mistaken for suspicious activity. Identify these processes and exclude their parent executables to prevent false alerts.
- Software installations or updates that require mounting filesystems in user directories might be flagged. Verify these activities and add the responsible parent executables to the exclusion criteria.
- Development tools that use temporary mounts for testing purposes can generate false positives. Recognize these tools and exclude their parent executables to reduce noise.
- Custom administrative scripts that perform legitimate mounting operations should be reviewed and, if deemed safe, their parent executables should be added to the exclusion list.

### Response and remediation

- Immediately isolate the affected system to prevent further data exfiltration or persistence by disconnecting it from the network.
- Terminate any suspicious mount processes identified in the alert to halt potential malicious activity.
- Conduct a thorough review of mounted filesystems and directories to identify and unmount any unauthorized or suspicious mounts.
- Restore any compromised files or directories from backups, ensuring they are clean and free from malicious modifications.
- Implement stricter access controls and permissions on sensitive directories like /tmp, /var/tmp, /dev/shm, /home, and /root to prevent unauthorized mounting.
- Escalate the incident to the security operations team for further investigation and to assess the scope of the threat, including potential lateral movement or additional compromised systems.
- Enhance monitoring and detection capabilities by configuring alerts for unusual mount activities and integrating threat intelligence feeds to identify similar tactics used by adversaries.

