---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Delegated Managed Service Account Modification by an Unusual User" prebuilt detection rule.
---

# Delegated Managed Service Account Modification by an Unusual User

## Triage and analysis

### Investigating Delegated Managed Service Account Modification by an Unusual User

### Possible investigation steps
- Examine the winlog.event_data.SubjectUserName field and verify if he is allowed and used to perform this kind of dMSA changes.
- Examine the winlog.event_data.AttributeValue field to verify the targeted account and if it's supposed to use dMSA.
- Examine if there are any recent dMSA account creation by the same winlog.event_data.SubjectUserName.
- Investigate the history of the identified user account to determine if there are any other suspicious activities or patterns of behavior.
- Collaborate with the IT or security team to determine if the changes were authorized or if further action is needed to secure the environment.

### False positive analysis

- Migration of legacy service accounts using delegated managed service account.

### Response and remediation

- Immediately disable the winlog.event_data.SubjectUserName account and revert all changes performed by that account.
- Identify and isolate the source machines from where the SubjectUserName is authenticating.
- Reset passwords for all accounts that were potentially affected or had their permissions altered, focusing on privileged accounts to prevent adversaries from regaining access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the scope of the breach, including identifying any other compromised systems or accounts.
- Review and update access control policies and security configurations to prevent similar attacks, ensuring that only authorized personnel have the ability to modify critical Active Directory objects or create OU child objects.
