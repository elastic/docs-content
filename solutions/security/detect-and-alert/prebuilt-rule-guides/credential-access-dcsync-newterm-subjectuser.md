---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "FirstTime Seen Account Performing DCSync" prebuilt detection rule.
---

# FirstTime Seen Account Performing DCSync

## Triage and analysis

### Investigating FirstTime Seen Account Performing DCSync

Active Directory replication is the process by which the changes that originate on one domain controller are automatically transferred to other domain controllers that store the same data.

Active Directory data consists of objects that have properties, or attributes. Each object is an instance of an object class, and object classes and their respective attributes are defined in the Active Directory schema. Objects are defined by the values of their attributes, and changes to attribute values must be transferred from the domain controller on which they occur to every other domain controller that stores a replica of an affected object.

Adversaries can use the DCSync technique that uses Windows Domain Controller's API to simulate the replication process from a remote domain controller, compromising major credential material such as the Kerberos krbtgt keys that are used legitimately for creating tickets, but also for forging tickets by attackers. This attack requires some extended privileges to succeed (DS-Replication-Get-Changes and DS-Replication-Get-Changes-All), which are granted by default to members of the Administrators, Domain Admins, Enterprise Admins, and Domain Controllers groups. Privileged accounts can be abused to grant controlled objects the right to DCsync/Replicate.

More details can be found on [Threat Hunter Playbook](https://threathunterplaybook.com/library/windows/active_directory_replication.html?highlight=dcsync#directory-replication-services-auditing) and [The Hacker Recipes](https://www.thehacker.recipes/ad/movement/credentials/dumping/dcsync).

This rule monitors for when a Windows Event ID 4662 (Operation was performed on an Active Directory object) with the access mask 0x100 (Control Access) and properties that contain at least one of the following or their equivalent Schema-Id-GUID (DS-Replication-Get-Changes, DS-Replication-Get-Changes-All, DS-Replication-Get-Changes-In-Filtered-Set) is seen in the environment for the first time in the last 15 days.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account and system owners and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Correlate security events 4662 and 4624 (Logon Type 3) by their Logon ID (`winlog.logon.id`) on the Domain Controller (DC) that received the replication request. This will tell you where the AD replication request came from, and if it came from another DC or not.
- Scope which credentials were compromised (for example, whether all accounts were replicated or specific ones).

### False positive analysis

- Administrators may use custom accounts on Azure AD Connect; investigate if this is part of a new Azure AD account setup, and ensure it is properly secured. If the activity was expected and there is no other suspicious activity involving the host or user, the analyst can dismiss the alert.
- Although replicating Active Directory (AD) data to non-Domain Controllers is not a common practice and is generally not recommended from a security perspective, some software vendors may require it for their products to function correctly. Investigate if this is part of a new product setup, and ensure it is properly secured. If the activity was expected and there is no other suspicious activity involving the host or user, the analyst can dismiss the alert.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- If the entire domain or the `krbtgt` user was compromised:
  - Activate your incident response plan for total Active Directory compromise which should include, but not be limited to, a password reset (twice) of the `krbtgt` user.
- Investigate how the attacker escalated privileges and identify systems they used to conduct lateral movement. Use this information to determine ways the attacker could regain access to the environment.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

