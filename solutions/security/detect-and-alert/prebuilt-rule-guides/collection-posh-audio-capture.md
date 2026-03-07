---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "PowerShell Suspicious Script with Audio Capture Capabilities" prebuilt detection rule.'
---

# PowerShell Suspicious Script with Audio Capture Capabilities

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating PowerShell Suspicious Script with Audio Capture Capabilities

This alert indicates PowerShell script block content associated with microphone recording or Windows multimedia audio capture routines. Because audio capture can expose sensitive conversations, prioritize investigation when the activity is unexpected for the user, host, or time of day, or when the script suggests local staging or external transfer.

#### Key alert fields to review

- `user.name`, `user.domain`, `user.id`: Account execution context for correlation, prioritization, and scoping.
- `host.name`, `host.id`: Host execution context for correlation, prioritization, and scoping.
- `powershell.file.script_block_text`: Script block content that matched the detection logic.
- `powershell.file.script_block_id`, `powershell.sequence`, `powershell.total`: Script block metadata to pivot to other fragments or reconstruct full script content when split across multiple events.
- `file.path`, `file.directory`, `file.name`: File-origin context when the script block is sourced from an on-disk file.
- `powershell.file.script_block_length`: Script block length (size) context.

#### Possible investigation steps

- Establish alert context and ownership:
  - Identify the execution context using `user.name`, `user.domain`, and `user.id`, and the impacted endpoint using `host.name` and `host.id`.
  - If `file.path` or `file.name` is populated, note the script origin and whether the location is expected for administrative scripts.

- Analyze `powershell.file.script_block_text` for capability and intent:
  - Determine whether the script enumerates devices, starts/stops recording, sets recording duration, or saves output.
  - Capture any referenced output paths, filenames, or extensions (for example, `.wav`) that may indicate where audio was written.
  - Look for higher-risk patterns in the same content, such as dynamic unmanaged API access (for example, `Add-Type` with `DllImport`), obfuscation, looping/retry logic, or cleanup routines (delete after save/upload).
  - Note any embedded remote destinations, credentials, or upload logic if present to support containment and scoping.

- Reconstruct full script content when the script block is split:
  - Pivot on `powershell.file.script_block_id` for the same endpoint and time window.
  - Rebuild the full content by ordering fragments with `powershell.sequence` and validating completeness with `powershell.total` before drawing conclusions from a single fragment.
  - Review nearby script blocks from the same `user.id` and `host.id` to identify configuration, helper functions, or follow-on actions not present in the matching fragment.

- Validate execution chain and likely launch method (if additional telemetry is available):
  - Correlate the alert time on `host.name` with process execution telemetry to identify the PowerShell host process and its parent process.
  - Assess whether the parent process and timing are consistent with expected user/admin activity on that host.
  - If the script content indicates remote execution, scheduled execution, or automation, review surrounding activity for corroborating evidence (repeated runs, multiple hosts, or multiple users).

- Assess evidence of audio collection and data handling:
  - If the script indicates an output location, correlate with file activity around `@timestamp` to identify newly created or modified files that could contain recorded audio.
  - Review `file.path` and `file.name` (when present) for suspicious or deceptive naming and whether the same artifact appears on multiple endpoints.
  - If the script references encoding or compression, consider that audio may be staged as non-audio file types; use distinctive filenames or directories from the script content to guide searches.

- Identify possible exfiltration or secondary objectives:
  - Review the script content for staging steps (chunking, encoding, archiving) and any explicit network transfer logic.
  - If remote destinations are present in the script content, correlate with network telemetry for outbound connections from the same host near the alert time and evaluate whether transfer volume and timing are consistent with audio data movement.

- Scope and prevalence:
  - Search for the same function names, API strings, or distinctive substrings from `powershell.file.script_block_text` across other endpoints to identify reuse.
  - Check whether the same `user.id` is associated with similar script blocks on multiple hosts, or whether multiple users on the same `host.id` exhibit similar activity.
  - If `file.name` is populated, look for the same filename and path patterns elsewhere to determine distribution.

### False positive analysis

- Benign scripts typically show consistent script content and stable provenance (reused script name/path and predictable execution patterns). Unexpected users, ad hoc locations, or one-off executions on user workstations increase suspicion.

### Response and remediation

- If malicious or unauthorized audio capture is suspected:
  - Contain the endpoint to prevent further collection and reduce the risk of data loss.
  - Preserve evidence: the full reconstructed script content (all fragments), related PowerShell events in the same time window, and any identified output or staging artifacts.
  - If audio files are discovered, handle them as potentially sensitive data per your incident response and privacy procedures.
  - Identify any remote destinations from the script content and take network containment actions appropriate for your environment.
  - Scope for related activity using `user.id`, `host.id`, and distinctive content from `powershell.file.script_block_text` to identify other affected endpoints or users.
  - Assess the associated account for compromise and take account-level containment actions (credential reset, session revocation, access review) when misuse is confirmed.

- If confirmed benign:
  - Document the business purpose, script owner, and expected execution scope (accounts, hosts, and schedule).
  - If the activity is legitimate but creating operational noise, add rule exceptions with narrowly scoped constraints based on stable attributes (consistent script content patterns, known script file path/name, and expected executing accounts) rather than broadly suppressing audio-related indicators.
