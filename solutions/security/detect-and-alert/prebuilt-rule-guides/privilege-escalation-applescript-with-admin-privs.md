---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Apple Scripting Execution with Administrator Privileges" prebuilt detection rule.
---

# Apple Scripting Execution with Administrator Privileges

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Apple Scripting Execution with Administrator Privileges

AppleScript, a scripting language for macOS, automates tasks by controlling applications and system functions. Adversaries may exploit it to execute scripts with elevated privileges, bypassing password prompts, to gain unauthorized access or escalate privileges. The detection rule identifies such misuse by monitoring the execution of AppleScript with admin rights, excluding benign parent processes like Electron, to flag potential threats.

### Possible investigation steps

- Review the process details to confirm the execution of 'osascript' with administrator privileges, focusing on the command line arguments to understand the script's intent.
- Investigate the parent process of 'osascript' to determine if it is a known and trusted application, ensuring it is not 'Electron' or any other excluded parent processes.
- Check the user account associated with the 'osascript' execution to verify if it is a legitimate account and assess if there are any signs of compromise or unauthorized access.
- Analyze recent system logs and user activity to identify any unusual behavior or patterns that coincide with the time of the alert.
- Correlate this event with other security alerts or incidents to determine if it is part of a broader attack or isolated incident.

### False positive analysis

- Known false positives may arise from legitimate applications that use AppleScript with administrator privileges for valid operations, such as software installers or system management tools.
- Exclude processes with benign parent applications like Electron, as specified in the rule, to reduce false positives from common development environments.
- Consider adding exceptions for other trusted applications that frequently use AppleScript with elevated privileges, ensuring they are verified and necessary for business operations.
- Regularly review and update the list of excluded applications to adapt to changes in software usage and maintain effective threat detection.
- Monitor the frequency and context of alerts to identify patterns that may indicate false positives, adjusting the detection rule as needed to minimize unnecessary alerts.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious osascript processes running with administrator privileges that were not initiated by known, legitimate applications.
- Review system logs and process execution history to identify any unauthorized changes or access that occurred during the incident.
- Revoke any compromised credentials or accounts that may have been used to execute the AppleScript with elevated privileges.
- Restore the system to a known good state from a backup taken before the unauthorized script execution, if necessary.
- Implement application whitelisting to prevent unauthorized scripts from executing with elevated privileges in the future.
- Escalate the incident to the security operations team for further investigation and to assess the need for additional security controls or monitoring enhancements.
