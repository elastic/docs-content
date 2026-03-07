---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Startup/Logon Script added to Group Policy Object" prebuilt detection rule.'
---

# Startup/Logon Script added to Group Policy Object

## Triage and analysis

### Investigating Startup/Logon Script added to Group Policy Object

Group Policy Objects (GPOs) can be used by attackers to instruct arbitrarily large groups of clients to execute specified commands at startup, logon, shutdown, and logoff. This is done by creating or modifying the `scripts.ini` or `psscripts.ini` files. The scripts are stored in the following paths:
  - `<GPOPath>\Machine\Scripts\`
  - `<GPOPath>\User\Scripts\`

#### Possible investigation steps

- This attack abuses a legitimate mechanism of Active Directory, so it is important to determine whether the activity is legitimate and the administrator is authorized to perform this operation.
- Retrieve the contents of the `ScheduledTasks.xml` file, and check the `<Command>` and `<Arguments>` XML tags for any potentially malicious commands or binaries.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Scope which objects may be compromised by retrieving information about which objects are controlled by the GPO.

### False positive analysis

- Verify if the execution is legitimately authorized and executed under a change management process.

### Related rules

- Group Policy Abuse for Privilege Addition - b9554892-5e0e-424b-83a0-5aef95aa43bf
- Scheduled Task Execution at Scale via GPO - 15a8ba77-1c13-4274-88fe-6bd14133861e

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- The investigation and containment must be performed in every computer controlled by the GPO, where necessary.
- Remove the script from the GPO.
- Check if other GPOs have suspicious scripts attached.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
