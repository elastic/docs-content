---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Apple Mail Rule Plist Modification" prebuilt detection rule.'
---

# Suspicious Apple Mail Rule Plist Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Apple Mail Rule Plist Modification

This detects non-Apple Mail processes creating or modifying the SyncedRules.plist that stores Apple Mail rules, a persistence path because rules can trigger actions on incoming mail. Attackers commonly drop a script to disk, then edit the rules file so a crafted email (often from an attacker-controlled sender or with a specific subject) launches that script when it arrives.

### Possible investigation steps

- Identify the application that modified the plist and validate its legitimacy by checking code signature, bundle path, quarantine/download origin, and recent installation history.  
- Diff the current SyncedRules.plist against a known-good or previous version (including backups/snapshots) to pinpoint what rule entries changed and when.  
- Decode and review the plist contents to find any rule actions that execute scripts/binaries or reference external paths, then record the exact target command/path.  
- Locate and inspect any referenced script or executable (hash, signature, contents, timestamps, and network indicators) and determine whether it is newly created or staged nearby.  
- Correlate the modification time with surrounding system activity (process tree, file writes in user Library paths, network connections, and recent email-related events) to determine whether this is persistence setup versus benign automation.

### False positive analysis

- After a macOS reinstall, user migration, or restore from backup, SyncedRules.plist may be recreated or overwritten by a non-Mail restore/migration process when Mail data is copied back into the user’s MailData directory.  
- User-initiated or administrative automation that standardizes, repairs, or deploys Mail rules can modify SyncedRules.plist via command-line file operations or plist editing outside of Mail.app, especially during initial user provisioning or troubleshooting.

### Response and remediation

- Isolate the affected Mac from the network and temporarily disable Apple Mail rule processing by moving `SyncedRules.plist` out of the MailData directory to prevent any rule-triggered script execution while preserving evidence.  
- Collect and preserve the modified `SyncedRules.plist`, its extended attributes/quarantine flags, and the modifying process binary/app bundle, then decode the plist to identify any rule actions that reference on-disk scripts or executables.  
- Remove malicious persistence by deleting the offending rule entries (or restoring `SyncedRules.plist` from a known-good backup) and deleting/quarantining any referenced scripts/binaries and their launch points if they were dropped on disk.  
- Hunt for and eradicate the originator by reviewing recently installed or unsigned apps and user-level agents/daemons that wrote into `~/Library/Mail/**/MailData/`, and reimage the endpoint if additional persistence or tampering is found.  
- Recover by re-enabling Mail with a clean ruleset, forcing credential/session resets for affected mail accounts, and monitoring for recurrence of `SyncedRules.plist` changes or rule-triggered execution when new mail arrives.  
- Escalate to incident response immediately if the plist contains rules invoking `sh`, `osascript`, `python`, or a non-Apple executable path, if the modifying process is unsigned/untrusted, or if the referenced script shows network beacons or data access behavior.
