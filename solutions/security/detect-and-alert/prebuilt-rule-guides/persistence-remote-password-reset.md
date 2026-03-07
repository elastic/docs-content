---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Account Password Reset Remotely" prebuilt detection rule.
---

# Account Password Reset Remotely

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Account Password Reset Remotely

Remote password resets are crucial for managing user accounts, especially for privileged users. However, adversaries exploit this by resetting passwords to maintain unauthorized access or bypass security policies. The detection rule identifies suspicious remote password resets by monitoring successful network logins and subsequent password reset actions, focusing on privileged accounts to minimize noise and highlight potential threats.

### Possible investigation steps

- Review the source IP address from the authentication event to determine if it is from a known or trusted network. Investigate any unfamiliar or suspicious IP addresses.
- Check the winlog.event_data.TargetUserName from the password reset event to confirm if it belongs to a privileged account and verify if the reset was authorized.
- Correlate the winlog.event_data.SubjectLogonId from both the authentication and password reset events to ensure they are linked and identify the user or process responsible for the actions.
- Investigate the timing and frequency of similar events to identify patterns or anomalies that may indicate malicious activity.
- Examine any recent changes or activities associated with the account in question to assess if there are other signs of compromise or unauthorized access.

### False positive analysis

- Routine administrative tasks can trigger false positives when legitimate IT staff reset passwords for maintenance or support. To manage this, create exceptions for known IT personnel or service accounts that frequently perform these actions.
- Automated scripts or tools used for account management might cause false alerts. Identify and exclude these scripts or tools by their specific account names or IP addresses.
- Scheduled password resets for compliance or security policies may appear suspicious. Document and exclude these scheduled tasks by their timing and associated accounts.
- Service accounts with naming conventions similar to privileged accounts might be flagged. Review and adjust the rule to exclude these specific service accounts by refining the naming patterns in the query.
- Internal network devices or systems that perform regular password resets could be misinterpreted as threats. Whitelist these devices by their IP addresses or hostnames to reduce noise.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Revoke any active sessions associated with the compromised account to disrupt any ongoing malicious activities.
- Reset the password of the affected account using a secure method, ensuring it is done from a trusted and secure system.
- Conduct a thorough review of recent account activities and system logs to identify any additional unauthorized changes or access attempts.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the scope of the breach.
- Implement additional monitoring on the affected account and related systems to detect any further suspicious activities.
- Review and update access controls and privileged account management policies to prevent similar incidents in the future.

## Performance
This rule may cause medium to high performance impact due to logic scoping all remote Windows logon activity.

