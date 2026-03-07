---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Persistence via Docker Shortcut Modification" prebuilt detection rule.'
---

# Persistence via Docker Shortcut Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Persistence via Docker Shortcut Modification

Docker shortcuts on macOS are managed through dock property lists, which define application launch behaviors. Adversaries may exploit this by altering these lists to redirect shortcuts to malicious applications, thus achieving persistence. The detection rule identifies unauthorized modifications to these property lists, excluding legitimate processes, to flag potential threats. This approach helps in pinpointing suspicious activities that could indicate persistence mechanisms being established by attackers.

### Possible investigation steps

- Review the alert details to identify the specific file path and process name involved in the modification of the com.apple.dock.plist file.
- Examine the process that triggered the alert by checking its parent process, command line arguments, and execution history to determine if it is associated with known malicious activity.
- Investigate the user account associated with the file modification to determine if there are any signs of compromise or unauthorized access.
- Check for any recent changes or anomalies in the user's environment, such as new applications installed or unexpected network connections, that could indicate further malicious activity.
- Correlate the event with other security alerts or logs from the same host to identify any patterns or additional indicators of compromise.
- If possible, restore the original com.apple.dock.plist file from a backup to ensure the system's integrity and prevent the execution of any malicious applications.

### False positive analysis

- Legitimate software updates or installations may modify the dock property list. Users can create exceptions for known update processes like software management tools to prevent false alerts.
- System maintenance tasks performed by macOS utilities might trigger the rule. Exclude processes such as cfprefsd and plutil, which are involved in regular system operations, to reduce noise.
- Custom scripts or automation tools that modify user preferences could be flagged. Identify and whitelist these scripts if they are part of routine administrative tasks.
- Security or IT management tools like Jamf or Kandji may interact with dock property lists. Ensure these tools are included in the exclusion list to avoid unnecessary alerts.
- User-initiated changes to dock settings can also be mistaken for malicious activity. Educate users on the implications of modifying dock settings and monitor for patterns that deviate from normal behavior.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further malicious activity or lateral movement.
- Terminate any suspicious processes identified as modifying the dock property list, especially those not matching legitimate process names or executables.
- Restore the original com.apple.dock.plist file from a known good backup to ensure the dock shortcuts are not redirecting to malicious applications.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection tools to identify and remove any additional malicious software.
- Review and audit user accounts and permissions on the affected system to ensure no unauthorized access or privilege escalation has occurred.
- Implement monitoring for any future unauthorized modifications to dock property lists, ensuring alerts are configured for quick response.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected.
