---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Symbolic Link to Shadow Copy Created" prebuilt detection rule.'
---

# Symbolic Link to Shadow Copy Created

## Triage and analysis

### Investigating Symbolic Link to Shadow Copy Created

Shadow copies are backups or snapshots of an endpoint's files or volumes while they are in use. Adversaries may attempt to discover and create symbolic links to these shadow copies in order to copy sensitive information offline. If Active Directory (AD) is in use, often the ntds.dit file is a target as it contains password hashes, but an offline copy is needed to extract these hashes and potentially conduct lateral movement.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Investigate the process execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence, whether they are located in expected locations, and if they are signed with valid digital signatures.
- Investigate other alerts associated with the user/host during the past 48 hours.
- Determine if a volume shadow copy was recently created on this endpoint.
- Review privileges of the end user as this requires administrative access.
- Verify if the ntds.dit file was successfully copied and determine its copy destination.
- Investigate for registry SYSTEM file copies made recently or saved via Reg.exe.
- Investigate recent deletions of volume shadow copies.
- Identify other files potentially copied from volume shadow copy paths directly.

### False positive analysis

- This rule should cause very few false positives. Benign true positives (B-TPs) can be added as exceptions if necessary.

### Related rules

- NTDS or SAM Database File Copied - 3bc6deaa-fbd4-433a-ae21-3e892f95624f

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- If the entire domain or the `krbtgt` user was compromised:
  - Activate your incident response plan for total Active Directory compromise which should include, but not be limited to, a password reset (twice) of the `krbtgt` user.
- Locate and remove static files copied from volume shadow copies.
- Command-Line tool mklink should require administrative access by default unless in developer mode.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
