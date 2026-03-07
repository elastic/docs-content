---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Group Policy Abuse for Privilege Addition" prebuilt detection rule.
---

# Group Policy Abuse for Privilege Addition

## Triage and analysis

### Investigating Group Policy Abuse for Privilege Addition

Group Policy Objects (GPOs) can be used to add rights and/or modify Group Membership on GPOs by changing the contents of an INF file named GptTmpl.inf, which is responsible for storing every setting under the Security Settings container in the GPO. This file is unique for each GPO, and only exists if the GPO contains security settings. Example Path: "\\DC.com\SysVol\DC.com\Policies\{PolicyGUID}\Machine\Microsoft\Windows NT\SecEdit\GptTmpl.inf"

#### Possible investigation steps

- This attack abuses a legitimate mechanism of Active Directory, so it is important to determine whether the activity is legitimate and the administrator is authorized to perform this operation.
- Retrieve the contents of the `GptTmpl.inf` file, and under the `Privilege Rights` section, look for potentially dangerous high privileges, for example: SeTakeOwnershipPrivilege, SeEnableDelegationPrivilege, etc.
- Inspect the user security identifiers (SIDs) associated with these privileges, and if they should have these privileges.

### False positive analysis

- Inspect whether the user that has done the modifications should be allowed to. The user name can be found in the `winlog.event_data.SubjectUserName` field.

### Related rules

- Scheduled Task Execution at Scale via GPO - 15a8ba77-1c13-4274-88fe-6bd14133861e
- Startup/Logon Script added to Group Policy Object - 16fac1a1-21ee-4ca6-b720-458e3855d046

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- The investigation and containment must be performed in every computer controlled by the GPO, where necessary.
- Remove the script from the GPO.
- Check if other GPOs have suspicious scripts attached.

