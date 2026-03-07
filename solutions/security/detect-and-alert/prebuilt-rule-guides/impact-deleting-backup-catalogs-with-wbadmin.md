---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Backup Deletion with Wbadmin" prebuilt detection rule.'
---

# Backup Deletion with Wbadmin

## Triage and analysis

### Investigating Backup Deletion with Wbadmin

Windows Server Backup stores the details about your backups (what volumes are backed up and where the backups are located) in a file called a backup catalog, which ransomware victims can use to recover corrupted backup files. Deleting these files is a common step in threat actor playbooks.

This rule identifies the deletion of the backup catalog using the `wbadmin.exe` utility.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Assess whether this behavior is prevalent in the environment by looking for similar occurrences across hosts.
- Check if any files on the host machine have been encrypted.

### False positive analysis

- Administrators can use this command to delete corrupted catalogs, but overall the activity is unlikely to be legitimate.

### Related rules

- Third-party Backup Files Deleted via Unexpected Process - 11ea6bec-ebde-4d71-a8e9-784948f8e3e9
- Volume Shadow Copy Deleted or Resized via VssAdmin - b5ea4bfe-a1b2-421f-9d47-22a75a6f2921
- Volume Shadow Copy Deletion via PowerShell - d99a037b-c8e2-47a5-97b9-170d076827c4
- Volume Shadow Copy Deletion via WMIC - dc9c1f74-dac3-48e3-b47f-eb79db358f57

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Consider isolating the involved host to prevent destructive behavior, which is commonly associated with this activity.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- If any other destructive action was identified on the host, it is recommended to prioritize the investigation and look for ransomware preparation and execution activities.
- If any backups were affected:
  - Perform data recovery locally or restore the backups from replicated copies (cloud, other servers, etc.).
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
