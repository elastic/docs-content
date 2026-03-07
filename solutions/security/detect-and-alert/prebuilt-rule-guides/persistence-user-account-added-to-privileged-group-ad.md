---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "User Added to Privileged Group in Active Directory" prebuilt detection rule.'
---

# User Added to Privileged Group in Active Directory

## Triage and analysis

### Investigating User Added to Privileged Group in Active Directory

Privileged accounts and groups in Active Directory are those to which powerful rights, privileges, and permissions are granted that allow them to perform nearly any action in Active Directory and on domain-joined systems.

Attackers can add users to privileged groups to maintain a level of access if their other privileged accounts are uncovered by the security team. This allows them to keep operating after the security team discovers abused accounts.

This rule monitors events related to a user being added to a privileged group.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should manage members of this group.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.

### False positive analysis

- This attack abuses a legitimate Active Directory mechanism, so it is important to determine whether the activity is legitimate, if the administrator is authorized to perform this operation, and if there is a need to grant the account this level of privilege.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- If the admin is not aware of the operation, activate your Active Directory incident response plan.
- If the user does not need the administrator privileges, remove the account from the privileged group.
- Review the privileges of the administrator account that performed the action.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
