---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Manual Dracut Execution" prebuilt detection rule.
---

# Manual Dracut Execution

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Manual Dracut Execution

Dracut is a utility in Linux systems used to create initramfs images, essential for booting. Adversaries might exploit Dracut to craft malicious initramfs, embedding backdoors for persistence. The detection rule identifies unusual Dracut executions by scrutinizing process origins and excluding legitimate parent processes, flagging potential unauthorized use.

### Possible investigation steps

- Review the process details to confirm the execution of the dracut command, focusing on the process.name and process.parent.executable fields to identify any unusual parent processes.
- Examine the command line arguments used with the dracut process by checking the process.parent.command_line field to understand the context of its execution.
- Investigate the user account associated with the dracut execution to determine if it aligns with expected administrative activity or if it indicates potential unauthorized access.
- Check the system logs and any related security alerts around the time of the dracut execution to identify any correlated suspicious activities or anomalies.
- Assess the system for any changes to the initramfs image or other boot-related files that could indicate tampering or the presence of backdoors.

### False positive analysis

- Legitimate system updates or kernel installations may trigger the rule. To handle this, users can create exceptions for processes originating from known update paths like /usr/lib/kernel/* or /etc/kernel/install.d/*.
- Automated scripts or maintenance tasks that use dracut for legitimate purposes might be flagged. Users should identify these scripts and add their parent process names, such as dracut-install or run-parts, to the exclusion list.
- Custom administrative scripts executed by trusted users could be mistaken for suspicious activity. Users can exclude specific command lines or arguments associated with these scripts, such as /usr/bin/dracut-rebuild, to prevent false positives.
- Temporary or testing environments where dracut is used for non-malicious testing purposes might trigger alerts. Users can exclude these environments by specifying unique parent process paths or names that are characteristic of the testing setup.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement or data exfiltration by the adversary.
- Terminate any suspicious or unauthorized dracut processes identified on the system to halt any ongoing malicious activity.
- Conduct a thorough review of the initramfs images on the affected system to identify and remove any unauthorized or malicious modifications.
- Restore the system's initramfs from a known good backup to ensure the integrity of the boot process.
- Implement monitoring for any future unauthorized dracut executions by setting up alerts for similar process activities, ensuring quick detection and response.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Review and update access controls and permissions to limit the ability to execute dracut to only authorized personnel, reducing the risk of future exploitation.
