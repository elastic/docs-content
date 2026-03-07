---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Directory Creation in /bin directory" prebuilt detection rule.'
---

# Directory Creation in /bin directory

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Directory Creation in /bin directory

The /bin directory is crucial for Linux systems, housing essential binaries for system operations. Adversaries may exploit this by creating directories here to conceal malicious files, leveraging the directory's trusted status. The detection rule identifies suspicious directory creation by monitoring 'mkdir' executions in critical binary paths, excluding legitimate system operations, thus flagging potential threats for further investigation.

### Possible investigation steps

- Review the process details to confirm the execution of 'mkdir' in the specified critical binary paths such as /bin, /usr/bin, /usr/local/bin, /sbin, /usr/sbin, and /usr/local/sbin.
- Check the parent process of the 'mkdir' command to determine if it was initiated by a legitimate system process or a potentially malicious one.
- Investigate the user account associated with the 'mkdir' process to assess if it has the necessary permissions and if the activity aligns with the user's typical behavior.
- Examine the system logs around the time of the directory creation for any other suspicious activities or anomalies that might indicate a broader attack.
- Verify if any files or executables have been placed in the newly created directory and assess their legitimacy and potential threat level.
- Cross-reference the event with threat intelligence sources to identify if the activity matches any known malicious patterns or indicators of compromise.

### False positive analysis

- System updates or package installations may trigger directory creation in the /bin directory as part of legitimate operations. Users can mitigate this by creating exceptions for known package management processes like apt, yum, or rpm.
- Custom scripts or administrative tasks that require creating directories in the /bin directory for temporary storage or testing purposes can also lead to false positives. Users should document and exclude these specific scripts or tasks from the detection rule.
- Automated deployment tools or configuration management systems such as Ansible, Puppet, or Chef might create directories in the /bin directory as part of their setup routines. Users should identify these tools and add them to the exclusion list to prevent unnecessary alerts.
- Development or testing environments where developers have permissions to create directories in the /bin directory for application testing can result in false positives. Users should differentiate between production and non-production environments and apply the rule accordingly.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement or data exfiltration by the adversary.
- Terminate any suspicious processes related to the directory creation in the /bin directory to halt any ongoing malicious activity.
- Conduct a thorough review of the newly created directories and files within the /bin directory to identify and remove any malicious binaries or scripts.
- Restore any altered or deleted legitimate binaries from a known good backup to ensure system integrity and functionality.
- Implement file integrity monitoring on critical system directories, including /bin, to detect unauthorized changes in real-time.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are compromised.
- Review and update access controls and permissions for the /bin directory to restrict unauthorized directory creation and enhance security posture.
