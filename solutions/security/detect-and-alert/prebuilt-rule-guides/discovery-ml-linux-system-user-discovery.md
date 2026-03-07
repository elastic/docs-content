---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Linux User Discovery Activity" prebuilt detection rule.
---

# Unusual Linux User Discovery Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Linux User Discovery Activity

In Linux environments, user discovery commands help identify active users and system owners, crucial for system management. However, adversaries exploit this by executing these commands from atypical user contexts, often indicating account compromise. The detection rule leverages machine learning to identify anomalies in user discovery activities, flagging potential threats for further investigation.

### Possible investigation steps

- Review the alert details to identify the specific user account and the command executed that triggered the alert.
- Check the login history and session details for the identified user account to determine if the activity aligns with their typical behavior or if it appears suspicious.
- Investigate the source IP address and hostname associated with the user session to verify if they are known and trusted within the organization.
- Examine recent changes to user permissions or group memberships for the identified account to detect any unauthorized modifications.
- Look for any additional unusual or unexpected commands executed by the same user account around the time of the alert to identify potential follow-up malicious activities.
- Correlate the alert with other security events or logs, such as authentication logs or network traffic, to gather more context and assess the scope of the potential compromise.

### False positive analysis

- System administrators performing routine checks may trigger the rule. To manage this, create exceptions for known admin accounts executing user discovery commands during regular maintenance windows.
- Automated scripts or monitoring tools that run user discovery commands can cause false positives. Identify these scripts and whitelist their execution paths or user accounts.
- Developers or IT staff conducting legitimate troubleshooting might be flagged. Document these activities and exclude specific user accounts or IP addresses from the rule.
- Scheduled tasks or cron jobs that include user discovery commands could be misinterpreted as threats. Review and exclude these tasks from the detection rule to prevent unnecessary alerts.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes associated with the unusual user discovery activity to halt potential malicious actions.
- Conduct a thorough review of the affected user account's recent activities and access logs to identify any unauthorized changes or access.
- Reset the credentials of the compromised account and any other accounts that may have been accessed using the compromised credentials.
- Implement additional monitoring on the affected system and user accounts to detect any further suspicious activities or attempts to regain access.
- Escalate the incident to the security operations team for a deeper investigation into potential related threats, such as credential dumping or privilege escalation attempts.
- Review and update access controls and permissions to ensure that only authorized users have access to sensitive systems and data, reducing the risk of future compromises.
