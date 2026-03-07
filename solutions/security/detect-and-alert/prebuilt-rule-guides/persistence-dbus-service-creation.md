---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "D-Bus Service Created" prebuilt detection rule.
---

# D-Bus Service Created

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating D-Bus Service Created

D-Bus is an inter-process communication system in Linux, enabling applications to communicate. Adversaries may exploit D-Bus by creating unauthorized service files to maintain persistence or escalate privileges. The detection rule identifies suspicious service file creations in key directories, excluding known legitimate processes, to flag potential malicious activity.

### Possible investigation steps

- Review the file path and extension to confirm if the created file is located in one of the monitored directories such as /usr/share/dbus-1/system-services/ or /etc/dbus-1/system.d/, and ensure it has a .service or .conf extension.
- Examine the process executable that created the file to determine if it is listed as a known legitimate process in the exclusion list. If not, investigate the process further to understand its origin and purpose.
- Check the process name and path for any unusual or unexpected patterns, especially if it is not part of the known exclusions like ssm-agent-worker or platform-python*.
- Investigate the file creation time and correlate it with other system activities or logs to identify any suspicious behavior or patterns around the time of the alert.
- Look into the user account associated with the process that created the file to determine if it has the necessary permissions and if the activity aligns with the user's typical behavior.
- Search for any related alerts or logs that might indicate a broader attack pattern, such as other unauthorized file creations or modifications in the system.

### False positive analysis

- Package manager operations can trigger false positives when legitimate service files are created during software installations or updates. To manage this, exclude processes associated with known package managers like dpkg, rpm, and yum from the detection rule.
- System service updates may also result in false positives. Exclude processes such as systemd and crond that are responsible for legitimate system service management.
- Development and testing environments often involve the creation of temporary or test service files. Exclude paths and processes specific to these environments, such as those under /tmp or /dev/fd, to reduce noise.
- Automation tools like Puppet and Chef can create service files as part of their configuration management tasks. Exclude these tools by adding their executable paths to the exception list.
- Custom scripts or tools that mimic package manager behavior might also cause false positives. Identify and exclude these specific scripts or tools by their process names or paths if they are known to be benign.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes associated with the creation of unauthorized D-Bus service files to halt potential malicious activity.
- Remove any unauthorized D-Bus service files identified in the specified directories to eliminate persistence mechanisms.
- Conduct a thorough review of user accounts and privileges on the affected system to ensure no unauthorized privilege escalation has occurred.
- Restore the system from a known good backup if unauthorized changes or damage to the system are detected.
- Monitor the system and network for any signs of re-infection or similar suspicious activities, using enhanced logging and alerting mechanisms.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
