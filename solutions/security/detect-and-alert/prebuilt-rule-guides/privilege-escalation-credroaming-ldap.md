---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Modification of the msPKIAccountCredentials" prebuilt detection rule.
---

# Modification of the msPKIAccountCredentials

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Modification of the msPKIAccountCredentials

The msPKIAccountCredentials attribute in Active Directory stores encrypted credential data, including private keys and certificates. Adversaries may exploit this by altering the attribute to escalate privileges, potentially overwriting files. The detection rule identifies such modifications by monitoring specific directory service events, focusing on changes to this attribute, excluding actions by the system account, thus highlighting unauthorized access attempts.

### Possible investigation steps

- Review the event logs for the specific event code 5136 to gather details about the modification event, including the timestamp and the user account involved.
- Examine the winlog.event_data.SubjectUserSid field to identify the user who attempted the modification, ensuring it is not the system account (S-1-5-18).
- Investigate the history and behavior of the identified user account to determine if there are any previous suspicious activities or anomalies.
- Check for any recent changes or anomalies in the affected Active Directory User Object, focusing on the msPKIAccountCredentials attribute.
- Assess the potential impact of the modification by identifying any files or systems that may have been affected by the altered credentials.
- Correlate this event with other security alerts or logs to identify any patterns or coordinated activities that might indicate a broader attack.

### False positive analysis

- Routine administrative tasks by IT personnel may trigger the rule. To manage this, create exceptions for specific user accounts or groups known to perform these tasks regularly.
- Scheduled maintenance scripts or automated processes that modify Active Directory attributes could be mistaken for unauthorized changes. Identify these processes and exclude their associated user accounts or service accounts from the rule.
- Software updates or installations that require changes to user credentials might cause false positives. Document these events and adjust the rule to ignore modifications during known update windows.
- Legitimate changes made by third-party applications integrated with Active Directory can be flagged. Review and whitelist these applications by excluding their associated user accounts or service accounts.
- Temporary changes during incident response or security audits may appear suspicious. Coordinate with security teams to ensure these activities are recognized and excluded from triggering alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Revoke any potentially compromised certificates and private keys associated with the affected msPKIAccountCredentials attribute to prevent misuse.
- Conduct a thorough review of recent changes in Active Directory, focusing on the msPKIAccountCredentials attribute, to identify any unauthorized modifications or access patterns.
- Reset passwords and regenerate keys for any accounts or services that may have been affected to ensure that compromised credentials are no longer valid.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the full scope of the breach.
- Implement additional monitoring on the affected systems and accounts to detect any further suspicious activity or attempts to exploit similar vulnerabilities.
- Review and update access controls and permissions in Active Directory to ensure that only authorized personnel have the ability to modify sensitive attributes like msPKIAccountCredentials.
