---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Interactive Logon by an Unusual Process" prebuilt detection rule.'
---

# Interactive Logon by an Unusual Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Interactive Logon by an Unusual Process

Interactive logons in Windows environments typically involve standard processes like winlogon.exe. Adversaries may exploit alternate processes to create tokens, escalating privileges and bypassing controls. This detection rule identifies anomalies by flagging logons via non-standard executables, focusing on mismatched user SIDs and unusual process paths, thus highlighting potential privilege escalation attempts.

### Possible investigation steps

- Review the process executable path to determine if it is a known or expected application for interactive logons. Investigate any unfamiliar or suspicious paths.
- Examine the SubjectUserSid and TargetUserSid to identify the users involved in the logon attempt. Check for any discrepancies or unusual patterns in user activity.
- Analyze the event logs around the time of the alert to identify any related or preceding events that might indicate how the unusual process was initiated.
- Investigate the system for any signs of compromise, such as unexpected changes in system files, unauthorized software installations, or other indicators of malicious activity.
- Check for any recent privilege escalation attempts or access token manipulations that might correlate with the alert, using the MITRE ATT&CK framework references for guidance.

### False positive analysis

- Legitimate administrative tools or scripts may trigger this rule if they use non-standard executables for logon processes. To manage this, identify and whitelist these known tools by adding their executable paths to the exception list.
- Custom applications developed in-house that require interactive logon might be flagged. Review these applications and, if verified as safe, exclude their executable paths from the detection rule.
- Automated tasks or services that use alternate credentials for legitimate purposes can cause false positives. Analyze these tasks and, if they are part of regular operations, adjust the rule to exclude their specific user SIDs or executable paths.
- Security software or monitoring tools that perform logon actions for scanning or auditing purposes may be incorrectly flagged. Confirm their legitimacy and add them to the exception list to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious processes identified as executing from non-standard paths that are not part of the legitimate Windows system processes.
- Revoke any tokens or credentials associated with the anomalous logon session to prevent further misuse.
- Conduct a thorough review of user accounts involved, focusing on any unauthorized privilege escalations or changes in permissions, and reset passwords as necessary.
- Analyze the system for any signs of persistence mechanisms or additional malware, and remove any identified threats.
- Restore the system from a known good backup if any unauthorized changes or malware are detected that cannot be easily remediated.
- Report the incident to the appropriate internal security team or management for further investigation and potential escalation to law enforcement if necessary.
