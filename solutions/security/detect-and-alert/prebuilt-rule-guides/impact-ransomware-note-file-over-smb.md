---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Ransomware Note File Dropped via SMB" prebuilt detection rule.'
---

# Potential Ransomware Note File Dropped via SMB

## Triage and analysis

## Performance

- This rule may cause medium to high performance impact due to logic scoping all icoming SMB network events.

#### Possible investigation steps

- Investigate the source.ip address connecting to port 445 on this host.
- Identify the user account that performed the file creation via SMB.
- If the number of files is too high and source.ip connecting over SMB is unusual isolate the host and block the used credentials.
- Investigate other alerts associated with the user/host during the past 48 hours.

### False positive analysis

- Remote file creation with similar file naming convention via SMB.


### Related rules

- Third-party Backup Files Deleted via Unexpected Process - 11ea6bec-ebde-4d71-a8e9-784948f8e3e9
- Volume Shadow Copy Deleted or Resized via VssAdmin - b5ea4bfe-a1b2-421f-9d47-22a75a6f2921
- Volume Shadow Copy Deletion via PowerShell - d99a037b-c8e2-47a5-97b9-170d076827c4
- Volume Shadow Copy Deletion via WMIC - dc9c1f74-dac3-48e3-b47f-eb79db358f57
- Suspicious File Renamed via SMB - 78e9b5d5-7c07-40a7-a591-3dbbf464c386

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Consider isolating the involved host to prevent destructive behavior, which is commonly associated with this activity.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- If any other destructive action was identified on the host, it is recommended to prioritize the investigation and look for ransomware preparation and execution activities.
- If any backups were affected:
  - Perform data recovery locally or restore the backups from replicated copies (cloud, other servers, etc.).
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
