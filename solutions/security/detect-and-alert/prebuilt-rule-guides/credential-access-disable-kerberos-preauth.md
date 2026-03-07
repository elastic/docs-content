---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kerberos Pre-authentication Disabled for User" prebuilt detection rule.
---

# Kerberos Pre-authentication Disabled for User

## Triage and analysis

### Investigating Kerberos Pre-authentication Disabled for User

Kerberos pre-authentication is an account protection against offline password cracking. When enabled, a user requesting access to a resource initiates communication with the Domain Controller (DC) by sending an Authentication Server Request (AS-REQ) message with a timestamp that is encrypted with the hash of their password. If and only if the DC is able to successfully decrypt the timestamp with the hash of the user’s password, it will then send an Authentication Server Response (AS-REP) message that contains the Ticket Granting Ticket (TGT) to the user. Part of the AS-REP message is signed with the user’s password. Microsoft's security monitoring [recommendations](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4738) state that `'Don't Require Preauth' – Enabled` should not be enabled for user accounts because it weakens security for the account’s Kerberos authentication.

AS-REP roasting is an attack against Kerberos for user accounts that do not require pre-authentication, which means that if the target user has pre-authentication disabled, an attacker can request authentication data for it and get a TGT that can be brute-forced offline, similarly to Kerberoasting.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Determine if the target account is sensitive or privileged.
- Inspect the account activities for suspicious or abnormal behaviors in the alert timeframe.

### False positive analysis

- Disabling pre-authentication is a bad security practice and should not be allowed in the domain. The security team should map and monitor any potential benign true positives (B-TPs), especially if the target account is privileged.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Reset the target account's password if there is any risk of TGTs having been retrieved.
- Re-enable the preauthentication option or disable the target account.
- Review the privileges assigned to the involved users to ensure that the least privilege principle is being followed.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

