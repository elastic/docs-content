---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Shadow Credentials added to AD Object" prebuilt detection rule.
---

# Potential Shadow Credentials added to AD Object

## Triage and analysis

### Investigating Potential Shadow Credentials added to AD Object

The msDS-KeyCredentialLink is an Active Directory (AD) attribute that links cryptographic certificates to a user or computer for domain authentication.

Attackers with write privileges on this attribute over an object can abuse it to gain access to the object or maintain persistence. This means they can authenticate and perform actions on behalf of the exploited identity, and they can use Shadow Credentials to request Ticket Granting Tickets (TGTs) on behalf of the identity.

#### Possible investigation steps

- Identify whether Windows Hello for Business (WHfB) and/or Azure AD is used in the environment.
  - Review the event ID 4624 for logon events involving the subject identity (`winlog.event_data.SubjectUserName`).
    - Check whether the `source.ip` is the server running Azure AD Connect.
- Contact the account and system owners and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Review the event IDs 4768 and 4769 for suspicious ticket requests involving the modified identity (`winlog.event_data.ObjectDN`).
  - Extract the source IP addresses from these events and use them as indicators of compromise (IoCs) to investigate whether the host is compromised and to scope the attacker's access to the environment.

### False positive analysis

- Administrators might use custom accounts on Azure AD Connect. If this is the case, make sure the account is properly secured. You can also create an exception for the account if expected activity makes too much noise in your environment.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
  - Remove the Shadow Credentials from the object.
- Investigate how the attacker escalated privileges and identify systems they used to conduct lateral movement. Use this information to determine ways the attacker could regain access to the environment.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

