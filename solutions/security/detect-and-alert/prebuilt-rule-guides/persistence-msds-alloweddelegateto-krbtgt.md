---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "KRBTGT Delegation Backdoor" prebuilt detection rule.
---

# KRBTGT Delegation Backdoor

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating KRBTGT Delegation Backdoor

In Active Directory, the KRBTGT account is crucial for Kerberos ticket granting. Adversaries may exploit this by altering the msDS-AllowedToDelegateTo attribute, enabling unauthorized ticket requests and persistent domain access. The detection rule identifies such modifications by monitoring specific event actions and codes, flagging high-risk changes to the KRBTGT delegation settings.

### Possible investigation steps

- Review the event logs for the specific event code 4738 to identify the user account that was modified and verify if the msDS-AllowedToDelegateTo attribute includes the KRBTGT service.
- Investigate the user account that performed the modification by checking their recent activities and login history to determine if the action was authorized or suspicious.
- Examine the timeline of the modification event to correlate it with any other unusual activities or alerts in the network around the same time.
- Check for any other modifications to sensitive attributes or accounts in Active Directory that might indicate a broader compromise.
- Assess the potential impact on the domain by evaluating the access level and permissions of the modified account and any associated systems or services.
- Consult with the IT security team to determine if there are any known maintenance activities or changes that could explain the modification, ensuring it was not a legitimate administrative action.

### False positive analysis

- Routine administrative tasks involving legitimate changes to the msDS-AllowedToDelegateTo attribute for service accounts may trigger alerts. Review the context of the change and verify with the IT team if it aligns with scheduled maintenance or updates.
- Automated scripts or tools used for Active Directory management might modify delegation settings as part of their operations. Identify these scripts and exclude their activity from triggering alerts by creating exceptions based on the script's signature or the account used.
- Changes made by trusted third-party applications that require delegation for functionality can be mistaken for malicious activity. Document these applications and adjust the detection rule to exclude their known and expected behavior.
- Regular audits or compliance checks that involve modifications to delegation settings should be accounted for. Coordinate with audit teams to schedule these activities and temporarily adjust monitoring rules to prevent false positives during these periods.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or ticket requests using the KRBTGT account.
- Revert any unauthorized changes to the msDS-AllowedToDelegateTo attribute for the KRBTGT account by restoring it to its previous state using a known good backup or manually resetting the attribute.
- Reset the KRBTGT account password twice to invalidate any existing Kerberos tickets that may have been issued using the compromised delegation settings.
- Conduct a thorough review of recent changes to user accounts and delegation settings in Active Directory to identify any other potential unauthorized modifications.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the scope of the compromise.
- Implement enhanced monitoring for changes to critical accounts and attributes in Active Directory, focusing on the KRBTGT account and similar high-value targets.
- Review and update access controls and delegation permissions to ensure that only authorized personnel have the ability to modify sensitive attributes like msDS-AllowedToDelegateTo.
