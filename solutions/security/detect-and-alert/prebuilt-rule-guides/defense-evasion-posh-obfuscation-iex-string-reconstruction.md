---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Dynamic IEX Reconstruction via Method String Access" prebuilt detection rule.
---

# Dynamic IEX Reconstruction via Method String Access

## Triage and analysis

> **Disclaimer**:
> This guide was created by humans with the assistance of generative AI. While its contents have been manually curated to include the most valuable information, always validate assumptions and adjust procedures to match your internal runbooks and incident triage and response policies.

### Investigating Dynamic IEX Reconstruction via Method String Access

This alert indicates PowerShell script block content that uses method-to-string conversion and indexed character extraction to assemble an execution primitive at runtime, commonly "IEX" (Invoke-Expression). This obfuscation technique can conceal dynamic execution intent and is often used to reduce obvious keywords in the script body.

#### Key alert fields to review

- `user.name`, `user.domain`, `user.id`: Account execution context for correlation, prioritization, and scoping.
- `host.name`, `host.id`: Host execution context for correlation, prioritization, and scoping.
- `file.path`, `file.directory`, `file.name`: File-origin context when the script block is sourced from an on-disk file.
- `powershell.file.script_block_text`: Script block content that matched the detection logic.
- `powershell.file.script_block_id`, `powershell.sequence`, `powershell.total`: Script block metadata to pivot to other fragments or reconstruct full script content when split across multiple events.
- `Esql.script_block_tmp`: Transformed script block where detection patterns replace original content with a marker to support scoring/counting and quickly spot match locations.
- `Esql.script_block_pattern_count`: Count of matches for the detection pattern(s) observed in the script block content.
- `powershell.file.script_block_entropy_bits`: Shannon entropy of the script block. Higher values may indicate obfuscation.
- `powershell.file.script_block_surprisal_stdev`: Standard deviation of surprisal across the script block. Low values indicate uniform randomness. High values indicate mixed patterns and variability.
- `powershell.file.script_block_unique_symbols`: Count of distinct characters present in the script block.
- `powershell.file.script_block_length`: Script block length (size) context.

#### Possible investigation steps

- Establish execution context and scope:
  - Review `host.name` and `host.id` to identify the affected endpoint and its role/criticality.
  - Review `user.name`, `user.domain`, and `user.id` to determine whether the activity aligns with expected administrative or automation usage.
  - Review `file.path`, `file.directory`, and `file.name` (when present) to understand whether the script originated from an on-disk file.
  - Review `agent.id` to pivot to other telemetry from the same endpoint and timeframe.

- Validate what matched and how extensively it appears:
  - Review `Esql.script_block_pattern_count` to gauge how often the technique appears within the script block (higher counts can indicate heavier obfuscation).
  - Use `Esql.script_block_tmp` to quickly locate the matched regions, then review the corresponding locations in `powershell.file.script_block_text` for the exact construct and nearby context.
  - Review `powershell.file.script_block_length` alongside `powershell.file.script_block_entropy_bits`, `powershell.file.script_block_surprisal_stdev`, and `powershell.file.script_block_unique_symbols` to help distinguish isolated string tricks from broader obfuscation.

- Reconstruct the full script block when content is split:
  - Pivot on `powershell.file.script_block_id` and order results by `powershell.sequence`.
  - Use `powershell.total` to confirm you have all fragments before making a final assessment.
  - Preserve the reassembled content from `powershell.file.script_block_text` for follow-on analysis and scoping.

- Determine the reconstructed token and follow-on behavior:
  - In `powershell.file.script_block_text`, identify the method string being indexed and the associated index list (for example, [n,n,n]) to determine what characters are being assembled.
  - Identify how the reconstructed string is used (for example, invoked directly, assigned to a variable, or passed as an argument) and what content it ultimately executes.
  - Capture any secondary artifacts referenced in the script content (for example, embedded payload strings, additional script blocks, or external resource locations) and use them to drive further correlation.

- Validate likely origin and initiating source:
  - If `file.path` is present, validate whether the script location is expected for the user and host, and whether it appears in a user-writable location or a standard administrative tooling path.
  - If file origin fields are not present, the script may have been executed interactively or generated at runtime; rely on surrounding endpoint telemetry to identify the initiating process and any related activity.

- Correlate with adjacent activity to understand impact:
  - Review other PowerShell script blocks on the same `host.id` and `user.id` around the alert time to identify staging steps and any follow-on execution.
  - If process telemetry is available, identify the PowerShell process and its parent process that initiated execution, and check for suspicious child processes near the alert time.
  - If network or file telemetry is available, look for downloads, outbound connections, and file writes temporally aligned with the script block execution and the content referenced within `powershell.file.script_block_text`.

- Assess prevalence across the environment:
  - Search for similar patterns (including stable substrings from `powershell.file.script_block_text`) across other hosts and users.
  - Prioritize results with higher `Esql.script_block_pattern_count` and higher obfuscation metrics to identify likely common tooling or shared payloads.

### False positive analysis

- PowerShell developers or automation teams may experiment with unconventional string manipulation, but method-string indexing to assemble execution primitives is uncommon in routine administration.
- Authorized security testing, malware analysis, or threat emulation activities can intentionally use this technique; validate against approved testing windows and operator accounts.
- Some script packaging or code protection approaches can introduce non-standard string operations; treat as benign only when the script origin (`file.path` / `file.name`), execution context (`user.id`), and surrounding host activity support a known, approved workflow.

### Response and remediation

- If malicious or suspicious activity is confirmed:
  - Contain the affected host identified by `host.id` to prevent additional execution and lateral movement.
  - Preserve evidence from the alert, including `powershell.file.script_block_text`, `powershell.file.script_block_id`, `powershell.sequence`, `powershell.total`, `file.path`, and `Esql.script_block_pattern_count`.
  - Scope for related activity by searching for similar content patterns across the environment and identifying additional impacted hosts and accounts.
  - If an on-disk script is involved (`file.path` present), collect the file for analysis and remove or quarantine it according to your incident handling process.
  - Review the associated account (`user.id`) for additional suspicious activity and remediate credential exposure as appropriate (for example, reset credentials and review recent authentication activity).

- If the activity is determined to be benign:
  - Document the legitimate script source, expected hosts, and operator accounts for future triage.
  - Reduce noise with narrowly scoped suppression using stable characteristics available in the alert (for example, consistent `file.path` and repeatable non-sensitive substrings in `powershell.file.script_block_text`), while continuing to monitor for deviations.

