---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Sensitive Privilege SeEnableDelegationPrivilege assigned to a User" prebuilt detection rule.'
---

# Sensitive Privilege SeEnableDelegationPrivilege assigned to a User

## Triage and analysis

### Investigating Sensitive Privilege SeEnableDelegationPrivilege assigned to a User

Kerberos delegation is an Active Directory feature that allows user and computer accounts to impersonate other accounts, act on their behalf, and use their privileges. Delegation (constrained and unconstrained) can be configured for user and computer objects.

Enabling unconstrained delegation for a computer causes the computer to store the ticket-granting ticket (TGT) in memory at any time an account connects to the computer, so it can be used by the computer for impersonation when needed. Risk is heightened if an attacker compromises computers with unconstrained delegation enabled, as they could extract TGTs from memory and then replay them to move laterally on the domain. If the attacker coerces a privileged user to connect to the server, or if the user does so routinely, the account will be compromised and the attacker will be able to pass-the-ticket to privileged assets.

SeEnableDelegationPrivilege is a user right that is controlled within the Local Security Policy of a domain controller and is managed through Group Policy. This setting is named **Enable computer and user accounts to be trusted for delegation**.

It is critical to control the assignment of this privilege. A user with this privilege and write access to a computer can control delegation settings, perform the attacks described above, and harvest TGTs from any user that connects to the system.

#### Possible investigation steps

- Investigate how the privilege was assigned to the user and who assigned it.
- Investigate other potentially malicious activity that was performed by the user that assigned the privileges using the `user.id` and `winlog.activity_id` fields as a filter during the past 48 hours.
- Investigate other alerts associated with the users/host during the past 48 hours.

### False positive analysis

- The SeEnableDelegationPrivilege privilege should not be assigned to users. If this rule is triggered in your environment legitimately, the security team should notify the administrators about the risks of using it.

### Related rules

- KRBTGT Delegation Backdoor - e052c845-48d0-4f46-8a13-7d0aba05df82

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Remove the privilege from the account.
- Review the privileges of the administrator account that performed the action.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
