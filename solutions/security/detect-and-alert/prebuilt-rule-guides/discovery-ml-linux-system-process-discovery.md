---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Linux Process Discovery Activity" prebuilt detection rule.
---

# Unusual Linux Process Discovery Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Linux Process Discovery Activity

In Linux environments, process discovery commands help users and administrators understand active processes, aiding in system management and troubleshooting. However, adversaries can exploit these commands to map running applications, potentially identifying vulnerabilities for privilege escalation or persistence. The detection rule leverages machine learning to identify atypical usage patterns, flagging potential threats when process discovery occurs from unexpected user contexts, thus helping to preemptively mitigate risks associated with compromised accounts.

### Possible investigation steps

- Review the user context from which the process discovery command was executed to determine if the user account is expected to perform such actions.
- Check the command history for the user account to identify any other unusual or unauthorized commands executed around the same time.
- Analyze the process discovery command details, including the specific command used and its parameters, to understand the intent and scope of the activity.
- Investigate the source IP address and host from which the command was executed to verify if it aligns with known and authorized devices for the user.
- Examine recent authentication logs for the user account to identify any suspicious login attempts or anomalies in login patterns.
- Correlate the activity with any other alerts or logs that might indicate a broader attack pattern or compromise, such as privilege escalation attempts or lateral movement.

### False positive analysis

- System administrators performing routine maintenance or troubleshooting may trigger the rule. To manage this, create exceptions for known administrator accounts or specific maintenance windows.
- Automated scripts or monitoring tools that regularly check system processes can be mistaken for unusual activity. Identify these scripts and whitelist their execution context to prevent false alerts.
- New software installations or updates might involve process discovery commands as part of their setup. Monitor installation activities and temporarily adjust the rule sensitivity during these periods.
- Developers or power users who frequently use process discovery commands for legitimate purposes can be excluded by adding their user accounts to an exception list, ensuring their activities do not trigger false positives.
- Training or testing environments where process discovery is part of normal operations should be configured with separate rules or exceptions to avoid unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the threat actor.
- Terminate any suspicious processes identified during the investigation to halt potential malicious activity.
- Change passwords for the compromised account and any other accounts that may have been accessed using the same credentials to prevent further unauthorized access.
- Conduct a thorough review of system logs and user activity to identify any additional signs of compromise or unauthorized access attempts.
- Restore the system from a known good backup if any malicious modifications or persistence mechanisms are detected.
- Implement additional monitoring on the affected system and similar environments to detect any recurrence of unusual process discovery activity.
- Escalate the incident to the security operations team for further analysis and to determine if broader organizational impacts need to be addressed.
