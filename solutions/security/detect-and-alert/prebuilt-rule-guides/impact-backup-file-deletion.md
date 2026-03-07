---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Third-party Backup Files Deleted via Unexpected Process" prebuilt detection rule.
---

# Third-party Backup Files Deleted via Unexpected Process

## Triage and analysis

### Investigating Third-party Backup Files Deleted via Unexpected Process

Backups are a significant obstacle for any ransomware operation. They allow the victim to resume business by performing data recovery, making them a valuable target.

Attackers can delete backups from the host and gain access to backup servers to remove centralized backups for the environment, ensuring that victims have no alternatives to paying the ransom.

This rule identifies file deletions performed by a process that does not belong to the backup suite and aims to delete Veritas or Veeam backups.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Check if any files on the host machine have been encrypted.

### False positive analysis

- This rule can be triggered by the manual removal of backup files and by removal using other third-party tools that are not from the backup suite. Exceptions can be added for specific accounts and executables, preferably tied together.

### Related rules

- Deleting Backup Catalogs with Wbadmin - 581add16-df76-42bb-af8e-c979bfb39a59
- Volume Shadow Copy Deleted or Resized via VssAdmin - b5ea4bfe-a1b2-421f-9d47-22a75a6f2921
- Volume Shadow Copy Deletion via PowerShell - d99a037b-c8e2-47a5-97b9-170d076827c4
- Volume Shadow Copy Deletion via WMIC - dc9c1f74-dac3-48e3-b47f-eb79db358f57

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Consider isolating the involved host to prevent destructive behavior, which is commonly associated with this activity.
- Perform data recovery locally or restore the backups from replicated copies (Cloud, other servers, etc.).
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

