---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Delete Volume USN Journal with Fsutil" prebuilt detection rule.'
---

# Delete Volume USN Journal with Fsutil

## Triage and analysis

### Investigating Delete Volume USN Journal with Fsutil

The Update Sequence Number (USN) Journal is a feature in the NTFS file system used by Microsoft Windows operating systems to keep track of changes made to files and directories on a disk volume. The journal records metadata for changes such as file creation, deletion, modification, and permission changes. It is used by the operating system for various purposes, including backup and recovery, file indexing, and file replication.

This artifact can provide valuable information in forensic analysis, such as programs executed (prefetch file operations), file modification events in suspicious directories, deleted files, etc. Attackers may delete this artifact in an attempt to cover their tracks, and this rule identifies the usage of the `fsutil.exe` utility to accomplish it.

Consider using the Elastic Defend integration instead of USN Journal, as the Elastic Defend integration provides more visibility and context in the file operations it records.

#### Possible investigation steps

- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Identify the user account that performed the action and whether it should perform this kind of action.
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate other alerts associated with the user/host during the past 48 hours.
  - Verify if any other anti-forensics behaviors were observed.
- Review file operation logs from Elastic Defend for suspicious activity the attacker tried to hide.

### False positive analysis

- This activity is unlikely to happen legitimately. Benign true positives (B-TPs) can be added as exceptions if necessary.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
