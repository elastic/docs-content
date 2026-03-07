---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious SIP Check by macOS Application" prebuilt detection rule.'
---

# Suspicious SIP Check by macOS Application

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious SIP Check by macOS Application

This rule detects a macOS application bundle launching `csrutil status` and explicitly parsing for “enabled,” an uncommon behavior that often signals preflight environment checks. Attackers use this to confirm System Integrity Protection constraints before deciding whether to attempt persistence, injection, or privilege escalation, or to abort execution to avoid analysis. A common pattern is a trojanized app from a mounted disk image performing the SIP check immediately after first launch, then conditionally unpacking and running a secondary payload.

### Possible investigation steps

- Identify the initiating application bundle and validate its provenance by reviewing its code signature, notarization status, Team ID, and download origin (e.g., Gatekeeper quarantine attributes and DMG mount source).  
- Build a short timeline around the SIP check to see what executed next from the same parent chain (new processes, scripts, installers, or command interpreters) and whether execution diverged after reading “enabled.”  
- Inspect the app’s bundle contents and related file activity for dropped binaries, launch agents/daemons, login items, or modified plist files that indicate persistence or staged payload execution.  
- Look for follow-on discovery and defense-evasion behavior on the host (e.g., VM/sandbox checks, system profiling, security tool enumeration, permission prompts abuse) that would support a malware preflight workflow.  
- If suspicious, isolate the host and collect the app bundle, associated DMG, and execution artifacts for detonation and reverse engineering, then hunt for the same app hash/Team ID across the fleet.

### False positive analysis

- A legitimate enterprise-managed macOS application performing a preflight compatibility or supportability check may invoke `csrutil status` and look for “enabled” to decide whether to proceed with installing drivers, configuring system settings, or enabling features that require SIP-related constraints awareness.  
- A user-initiated security/compliance workflow from a GUI app (e.g., a system configuration, diagnostic, or remediation utility distributed as an `.app` from `/Applications` or a mounted volume) may run `csrutil status` and parse for “enabled” to display a health report or to gate remediation instructions without any malicious follow-on activity.

### Response and remediation

- Isolate the affected macOS host from the network and prevent further execution by quitting the initiating `.app` and blocking its bundle identifier/hash via MDM/EDR policy.  
- Acquire and preserve artifacts for analysis, including the full `.app` bundle, the originating DMG/ZIP (if launched from `/Volumes`), Gatekeeper quarantine metadata, and recent install logs to trace the download source and execution chain.  
- Eradicate by removing the suspicious application and any follow-on components it created (new LaunchAgents/LaunchDaemons, Login Items, cron entries, and dropped executables in user and system Library paths), then terminate any child processes spawned after the SIP check.  
- Recover by reinstalling trusted software from known-good sources, rotating credentials used on the host since the first execution, and monitoring for re-creation of persistence files or repeated `csrutil status` checks from application bundles.  
- Escalate to incident response if the app is unsigned/notarization-failed, originates from a mounted volume or user Downloads, or if post-check activity includes attempts to modify security settings, write to persistence locations, or launch interpreters like `bash`, `zsh`, `python`, or `osascript`.  
- Harden by enforcing only notarized/signed app execution (Gatekeeper/MDM restrictions), blocking untrusted apps from removable/mounted volumes, and deploying detections for app-bundled execution of `csrutil` and subsequent persistence creation.
