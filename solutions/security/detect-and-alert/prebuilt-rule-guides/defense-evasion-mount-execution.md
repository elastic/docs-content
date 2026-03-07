---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Hidden Process via Mount Hidepid" prebuilt detection rule.
---

# Potential Hidden Process via Mount Hidepid

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Hidden Process via Mount Hidepid

The 'hidepid' mount option in Linux allows users to restrict visibility of process information in the /proc filesystem, enhancing privacy by limiting process visibility to the owner. Adversaries exploit this by remounting /proc with 'hidepid=2', concealing their processes from non-root users and evading detection tools like ps or top. The detection rule identifies such activity by monitoring for the execution of the mount command with specific arguments, flagging potential misuse for further investigation.

### Possible investigation steps

- Review the alert details to confirm the presence of the 'mount' process execution with arguments indicating '/proc' and 'hidepid=2'.
- Check the user account associated with the process execution to determine if it is a legitimate administrative user or a potential adversary.
- Investigate the parent process of the 'mount' command to understand the context and origin of the execution, ensuring it is not part of a known or legitimate administrative script.
- Examine recent login activity and user sessions on the host to identify any unauthorized access or suspicious behavior around the time of the alert.
- Analyze other processes running on the system to identify any hidden or suspicious activities that might be related to the use of 'hidepid=2'.
- Review system logs and audit logs for any additional indicators of compromise or related suspicious activities that coincide with the alert.

### False positive analysis

- System administrators or automated scripts may remount /proc with hidepid=2 for legitimate privacy or security reasons. To handle this, create exceptions for known administrative scripts or users by excluding their specific command lines or user IDs.
- Some security tools or monitoring solutions might use hidepid=2 as part of their normal operation to enhance system security. Identify these tools and exclude their processes from triggering alerts by adding them to an allowlist.
- Cloud environments or containerized applications might use hidepid=2 to isolate processes for multi-tenant security. Review the environment's standard operating procedures and exclude these known behaviors from detection.
- Regular system updates or maintenance scripts might temporarily use hidepid=2. Document these occurrences and adjust the detection rule to ignore these specific maintenance windows or scripts.
- If using a specific Linux distribution that employs hidepid=2 by default for certain operations, verify these defaults and configure the detection rule to exclude them.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Use root privileges to remount the /proc filesystem without the 'hidepid=2' option to restore visibility of all processes.
- Conduct a thorough review of running processes and system logs to identify any unauthorized or suspicious activities that may have been concealed.
- Terminate any identified malicious processes and remove any associated files or scripts from the system.
- Change all system and user passwords to prevent unauthorized access, especially if credential theft is suspected.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and alerting for future attempts to use the 'hidepid' option, ensuring rapid detection and response.
