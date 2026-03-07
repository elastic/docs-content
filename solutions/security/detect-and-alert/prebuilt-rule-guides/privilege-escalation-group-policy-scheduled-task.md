---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Scheduled Task Execution at Scale via GPO" prebuilt detection rule.'
---

# Scheduled Task Execution at Scale via GPO

## Triage and analysis

### Investigating Scheduled Task Execution at Scale via GPO

Group Policy Objects (GPOs) can be used by attackers to execute scheduled tasks at scale to compromise objects controlled by a given GPO. This is done by changing the contents of the `<GPOPath>\Machine\Preferences\ScheduledTasks\ScheduledTasks.xml` file.

#### Possible investigation steps

- This attack abuses a legitimate mechanism of Active Directory, so it is important to determine whether the activity is legitimate and the administrator is authorized to perform this operation.
- Retrieve the contents of the `ScheduledTasks.xml` file, and check the `<Command>` and `<Arguments>` XML tags for any potentially malicious commands or binaries.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Scope which objects may be compromised by retrieving information about which objects are controlled by the GPO.

### False positive analysis

- Verify if the execution is allowed and done under change management, and if the execution is legitimate.

### Related rules

- Group Policy Abuse for Privilege Addition - b9554892-5e0e-424b-83a0-5aef95aa43bf
- Startup/Logon Script added to Group Policy Object - 16fac1a1-21ee-4ca6-b720-458e3855d046

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- The investigation and containment must be performed in every computer controlled by the GPO, where necessary.
- Remove the script from the GPO.
- Check if other GPOs have suspicious scheduled tasks attached.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
