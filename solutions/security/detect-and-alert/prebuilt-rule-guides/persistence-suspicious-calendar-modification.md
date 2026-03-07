---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Calendar File Modification" prebuilt detection rule.'
---

# Suspicious Calendar File Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Calendar File Modification

Calendar files on macOS can be manipulated to trigger events, potentially allowing adversaries to execute malicious programs at set intervals, thus achieving persistence. This detection rule identifies unusual processes modifying calendar files, excluding known legitimate applications. By focusing on unexpected executables altering these files, it helps uncover potential threats exploiting calendar notifications for malicious purposes.

### Possible investigation steps

- Review the process executable path that triggered the alert to determine if it is a known or unknown application, focusing on paths not excluded by the rule.
- Examine the modification timestamp of the calendar file to correlate with any known user activity or scheduled tasks that might explain the change.
- Check the user account associated with the file modification to assess if the activity aligns with typical user behavior or if it suggests unauthorized access.
- Investigate any recent installations or updates of applications on the system that might have introduced new or unexpected executables.
- Look for additional indicators of compromise on the host, such as unusual network connections or other file modifications, to assess if the calendar file change is part of a broader attack.

### False positive analysis

- Legitimate third-party calendar applications may modify calendar files as part of their normal operation. Users can create exceptions for these known applications by adding their executable paths to the exclusion list.
- Automated backup or synchronization tools might access and modify calendar files. Identify these tools and exclude their processes to prevent false alerts.
- User scripts or automation workflows that interact with calendar files for personal productivity purposes can trigger this rule. Review and whitelist these scripts if they are verified as non-malicious.
- System updates or maintenance tasks occasionally modify calendar files. Monitor the timing of such events and correlate them with known update schedules to differentiate between legitimate and suspicious activities.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential lateral movement or further execution of malicious programs.
- Terminate any suspicious processes identified as modifying calendar files that are not part of the known legitimate applications list.
- Restore the calendar files from a known good backup to ensure no malicious events are scheduled.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious software.
- Review and audit user accounts and permissions on the affected system to ensure no unauthorized access or privilege escalation has occurred.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if other systems may be affected.
- Implement additional monitoring and alerting for unusual calendar file modifications across the network to enhance detection of similar threats in the future.
