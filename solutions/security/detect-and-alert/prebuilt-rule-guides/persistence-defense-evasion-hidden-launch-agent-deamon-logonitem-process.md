---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Hidden Child Process of Launchd" prebuilt detection rule.'
---

# Suspicious Hidden Child Process of Launchd

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Hidden Child Process of Launchd

Launchd is a key macOS system process responsible for managing system and user services. Adversaries may exploit it by creating hidden child processes to maintain persistence or evade defenses. The detection rule identifies unusual child processes of launchd, focusing on hidden files, which are often indicative of malicious activity. By monitoring process initiation events, it helps uncover potential threats linked to persistence and defense evasion tactics.

### Possible investigation steps

- Review the process details to identify the hidden child process, focusing on the process.name field to determine if it matches known malicious patterns or unusual names.
- Examine the process.parent.executable field to confirm that the parent process is indeed /sbin/launchd, ensuring the alert is not a false positive.
- Investigate the file path and attributes of the hidden file associated with the child process to determine its origin and legitimacy.
- Check the user account associated with the process initiation event to assess if it aligns with expected user behavior or if it indicates potential compromise.
- Correlate the event with other recent process initiation events on the same host to identify any patterns or additional suspicious activities.
- Review system logs and other security alerts for the host to gather more context on the potential threat and assess the scope of the activity.

### False positive analysis

- System updates or legitimate software installations may trigger hidden child processes of launchd. Users can create exceptions for known update processes or trusted software installations to prevent unnecessary alerts.
- Some legitimate applications may use hidden files for configuration or temporary data storage, which could be misidentified as suspicious. Users should identify these applications and whitelist their processes to reduce false positives.
- Development tools or scripts that run as background processes might appear as hidden child processes. Developers can exclude these tools by specifying their process names or paths in the detection rule exceptions.
- Automated backup or synchronization services might create hidden files as part of their normal operation. Users should verify these services and add them to an exclusion list if they are deemed safe.
- Custom scripts or automation tasks scheduled to run at login could be flagged. Users should review these scripts and, if legitimate, configure the rule to ignore these specific processes.

### Response and remediation

- Isolate the affected macOS system from the network to prevent further spread or communication with potential command and control servers.
- Terminate the suspicious hidden child process of launchd to stop any ongoing malicious activity.
- Conduct a thorough review of all launch agents, daemons, and logon items on the affected system to identify and remove any unauthorized or malicious entries.
- Restore the system from a known good backup if available, ensuring that the backup predates the initial compromise.
- Update the macOS system and all installed applications to the latest versions to patch any vulnerabilities that may have been exploited.
- Monitor the system for any signs of re-infection or further suspicious activity, focusing on process initiation events and hidden files.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected.
