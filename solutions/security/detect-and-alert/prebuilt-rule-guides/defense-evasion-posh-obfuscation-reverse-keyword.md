---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential PowerShell Obfuscation via Reverse Keywords" prebuilt detection rule.
---

# Potential PowerShell Obfuscation via Reverse Keywords

## Triage and analysis

> **Disclaimer**:
> This guide was created by humans with the assistance of generative AI. While its contents have been manually curated to include the most valuable information, always validate assumptions and adjust procedures to match your internal runbooks and incident triage and response policies.

### Investigating Potential PowerShell Obfuscation via Reverse Keywords

This alert indicates PowerShell script block content contains multiple reversed keyword strings commonly associated with execution, string manipulation, environment discovery, or networking. Reversing strings is frequently paired with runtime reconstruction (for example, reversing character arrays or joining string fragments) to reduce readability and evade simple content inspection.

Determine whether the script is part of expected administrative automation, software tooling, or an unauthorized execution chain. Prioritize analysis that reconstructs the full script, deobfuscates the reversed tokens, and identifies any follow-on behaviors such as dynamic execution, network access, or system discovery.

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

- Identify the execution scope and ownership:
  - Review `host.name` / `host.id` to confirm the affected endpoint and its criticality.
  - Review `user.id` (and `user.name` / `user.domain` if available) to understand the account context and whether this user is expected to run PowerShell on this host.
- Prioritize based on obfuscation signals:
  - Review `Esql.script_block_pattern_count`; higher counts suggest more extensive keyword hiding and can increase suspicion.
  - Use `powershell.file.script_block_length`, `powershell.file.script_block_entropy_bits`, `powershell.file.script_block_unique_symbols`, and `powershell.file.script_block_surprisal_stdev` to gauge how heavily obfuscated or machine-generated the content may be (treat these as supporting context, not proof of maliciousness).
- Reconstruct the full script content when split:
  - If `powershell.total` is greater than 1, retrieve all events with the same `powershell.file.script_block_id` and order them by `powershell.sequence` to rebuild the complete script block content.
  - Preserve both the reconstructed script and the original per-event `powershell.file.script_block_text` to maintain context and ordering.
- Deobfuscate and interpret intent:
  - Review `powershell.file.script_block_text` for reversed tokens and reverse them to identify the intended keywords and operations (for example, indicators of dynamic execution, downloads, socket/connection handling, WMI usage, or Win32 references).
  - Look for runtime string reconstruction patterns in the script content (for example, joins, character array operations, or replace operations) that turn reversed fragments into executable commands or parameters.
  - Use `Esql.script_block_tmp` to quickly locate the matched areas, then validate findings against `powershell.file.script_block_text`.
- Evaluate file-origin context (when present):
  - Review `file.path` (and `file.directory` / `file.name` if available) to determine whether the script is associated with an on-disk file and whether that location aligns with your organization's expected script locations and deployment practices.
  - If an on-disk script is indicated, coordinate collection of the referenced file for offline analysis and determine whether it is present on other systems.
- Extract and operationalize indicators:
  - From `powershell.file.script_block_text`, extract any embedded indicators such as hostnames, IP addresses, URLs, ports, file paths, or encoded blobs.
  - Use extracted indicators to scope for related activity on the same `host.id` and across other hosts where the same `user.id` is active, focusing on the alert timeframe and immediately adjacent activity.
- Correlate with adjacent telemetry to identify the execution chain and impact (as available in your environment):
  - Process activity: identify the PowerShell host process and the initiating parent process to understand whether execution was interactive, scheduled, or launched by another program.
  - Network activity: look for outbound connections aligned with the alert timestamp, especially if deobfuscated content suggests downloads or socket connections.
  - File and registry activity: look for payload staging, new or modified files, or persistence-related changes that occur shortly after the script block execution.
  - Authentication activity: review for suspicious logons, remote session creation, or lateral movement attempts around the same time on the affected host.
- Determine severity and next actions:
  - If the deobfuscated content indicates remote retrieval, execution of downloaded content, credential access, persistence, or lateral movement, treat the alert as potentially malicious and escalate for response.
  - If the script appears benign, document the validated purpose, expected owner, and any recurring identifiers (such as file location patterns) to support future triage.

### False positive analysis

- Internal scripts or tooling may use reversed strings as lightweight obfuscation to conceal configuration values or reduce casual readability. Validate the script's ownership, change history, and whether its presence and execution timing are expected for `host.id` and `user.id`.
- Commercial software, endpoint management agents, or security tooling may generate or embed obfuscated PowerShell during installation, updates, or health checks. Validate whether the activity aligns with known maintenance windows, expected endpoints, and consistent script content and `file.path` patterns.
- Authorized security testing may intentionally use string reversal. Confirm the scope, timing, and target hosts with the appropriate stakeholders before closing the alert.

### Response and remediation

- If activity is suspicious or unauthorized, contain the affected host to prevent further script execution and potential follow-on actions.
- Preserve evidence:
  - Retain the full `powershell.file.script_block_text` (including all segments reconstructed via `powershell.file.script_block_id`, `powershell.sequence`, and `powershell.total`).
  - Retain `file.path` context and the alert metadata needed to pivot (such as `host.id` and `user.id`).
- Identify and remediate the execution source:
  - Determine how PowerShell was launched (interactive, scheduled, or by another process) using correlated telemetry, and remove the triggering mechanism.
  - If an on-disk script is involved, remediate the file at `file.path` and any associated payloads or artifacts identified during analysis.
- Scope and hunt:
  - Search for the same or similar obfuscated content and extracted indicators across other endpoints, prioritizing systems accessed by the same `user.id` and systems with similar `file.path` patterns.
- Account actions:
  - If account misuse is suspected, follow organizational procedures to contain the account (for example, credential reset and session revocation) and review recent activity for additional suspicious behavior.
- Recovery and hardening:
  - Verify PowerShell logging coverage and retention are sufficient for incident response, and monitor for recurrence of similar reversed-keyword patterns on affected hosts and users.

