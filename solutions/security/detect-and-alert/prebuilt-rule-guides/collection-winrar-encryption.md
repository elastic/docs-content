---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Encrypting Files with WinRar or 7z" prebuilt detection rule.
---

# Encrypting Files with WinRar or 7z

## Triage and analysis

### Investigating Encrypting Files with WinRar or 7z

Attackers may compress and/or encrypt data collected before exfiltration. Compressing data can help stage and obfuscate content and may reduce the amount of data sent over the network. Encryption can be used to hide the contents of the archive and make the activity less apparent during review.

These steps are often performed in preparation for exfiltration, meaning the intrusion may be in its later stages.

#### Possible investigation steps

- Review the process ancestry (parent process tree) for the archiving command. Identify what launched WinRAR/7-Zip and whether the parent is expected in your environment.
- Validate the executable: check file path, signature, hash prevalence, and whether the binary is the expected vendor build.
- Identify the archive output location and name. Look for staging locations (e.g., user profile temp directories, public folders, removable media paths) and unusual naming patterns.
- Retrieve the created archive if policy allows. Determine whether the contents are sensitive or business-critical.
- Check whether the encryption password is present in the command line. If present, treat as high confidence data staging.
- If the password is not available and the archive format is `.zip` (or WinRAR is not using the `-hp` option), enumerate filenames within the archive to understand what was staged.
- Review other alerts and related activity for the same host/user over the last 48 hours (credential access, discovery, lateral movement, and outbound transfers).
- Investigate whether the archive was transferred off-host (e.g., browser uploads, cloud sync clients, RMM tools, SMB to unusual destinations, or other outbound network activity).

### False positive analysis

- Backup, packaging, and software distribution workflows may legitimately create password-protected archives.
- IT administrators and automation may use WinRAR/7-Zip for log collection, incident response packaging, or data transfer.
- Validate the parent process and context using `process.parent.executable` and `process.parent.command_line`, and confirm whether the archive destination and file set match an expected workflow.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Prioritize cases that involve personally identifiable information (PII) or other classified data.
- Isolate the involved hosts to prevent further post-compromise behavior.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

