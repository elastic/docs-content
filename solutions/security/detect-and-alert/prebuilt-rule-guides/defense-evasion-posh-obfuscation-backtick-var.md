---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential PowerShell Obfuscation via Backtick-Escaped Variable Expansion" prebuilt detection rule.
---

# Potential PowerShell Obfuscation via Backtick-Escaped Variable Expansion

## Triage and analysis

> **Disclaimer**:
> This guide was created by humans with the assistance of generative AI. While its contents have been manually curated to include the most valuable information, always validate assumptions and adjust procedures to match your internal runbooks and incident triage and response policies.

### Investigating Potential PowerShell Obfuscation via Backtick-Escaped Variable Expansion

This rule identifies Windows PowerShell Script Block Logging events where backtick-escaped characters are embedded within `${}` variable expansion. This technique can be used to split tokens and reconstruct variable names or keywords at runtime, reducing the effectiveness of simple string-based detections and content scanning.

Focus analysis on (1) who executed the script, (2) where it executed, (3) how much of the script is obfuscated, and (4) what the script ultimately does after deobfuscation. Higher `Esql.script_block_pattern_count`, elevated `powershell.file.script_block_entropy_bits`, and unexpected script origin (for example, unusual `file.path`) increase the likelihood of malicious intent.

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

- Validate execution scope and context:
  - Review `host.name` / `host.id` to understand where the script ran and whether the endpoint role makes this activity unexpected.
  - Review `user.name`, `user.domain`, and `user.id` to determine whether the account is expected to run PowerShell on this host and to identify any unusual account usage patterns in your environment.
  - If `file.path` / `file.name` / `file.directory` are present, determine whether the script appears to originate from an expected location (for example, a managed scripts directory) versus an unusual or user-writable location.

- Reconstruct the complete script before interpreting intent:
  - Pivot on `powershell.file.script_block_id` and collect all related fragments.
  - Use `powershell.sequence` and `powershell.total` to verify you have the full set of fragments and to order them correctly.
  - Review the reconstructed `powershell.file.script_block_text` for staging behavior (for example, an initial deobfuscation routine followed by a second stage that performs the primary action).

- Locate the obfuscated variable expansions and normalize the content:
  - Use `Esql.script_block_tmp` to quickly identify the positions of suspicious `${}` expansions, then review the corresponding sections in `powershell.file.script_block_text`.
  - Use `Esql.script_block_pattern_count` to estimate how pervasive the obfuscation is. A higher count is more consistent with deliberate evasion than isolated escaping.
  - In the matched `${}` segments, assess what the obfuscated expansion is intended to represent by mentally removing backtick escapes and looking for recognizable tokens (cmdlet/function names, variable names, or string literals) that the script is trying to hide.

- Assess behavior indicated by the script content:
  - Identify whether the script uses dynamic invocation patterns, such as building an invocation target at runtime or executing reconstructed strings.
  - Look for decoding and deobfuscation constructs (string concatenation, character-by-character reconstruction, data transformation, decompression) that may reveal embedded or second-stage content.
  - Extract and document any clear indicators contained in the script text (remote endpoints, file paths, registry paths, service/task names, or additional scripts referenced). Use these indicators to scope impact across hosts.

- Use alert-side obfuscation metrics to prioritize and focus review:
  - Compare `powershell.file.script_block_entropy_bits`, `powershell.file.script_block_unique_symbols`, and `powershell.file.script_block_surprisal_stdev` against what is typical in your environment for administrative scripts.
  - Treat scripts with high entropy and many unique symbols as higher risk, especially when combined with multiple obfuscated `${}` expansions.

- Scope prevalence and recurrence:
  - Search for other Script Block Logging events on the same `host.id` and `user.id` that include similar backtick-escaped `${}` patterns.
  - Look for repeated occurrences of the same `file.name` / `file.path` across multiple hosts, which may indicate a shared script or distributed execution.
  - If the script contains unique strings or indicators, use them to identify additional affected endpoints.

### False positive analysis

- Legitimate scripts that implement complex string building or variable-name handling and happen to use backticks within `${}` expansion (more common in developer tooling, templating, or edge-case input handling).
- Auto-generated PowerShell produced by administrative automation that uses nonstandard escaping or runtime string construction.

When evaluating potential false positives, weigh consistency (same `user.id`, `host.id`, and `file.path` over time) against indicators of compromise (unexpected user/host pairing, high obfuscation density, high entropy, or evidence of follow-on actions).

### Response and remediation

- If the activity is suspicious or confirmed malicious:
  - Contain the affected endpoint to prevent additional execution and limit potential lateral movement.
  - Preserve evidence from the alert, including the full reconstructed `powershell.file.script_block_text`, `powershell.file.script_block_id`, `powershell.sequence` / `powershell.total`, and any `file.path` / `file.name` values.
  - If an on-disk source is indicated by `file.path`, collect the referenced script and related files for review and remove or quarantine malicious artifacts according to your procedures.
  - Investigate for follow-on effects suggested by the script content (persistence, payload delivery, configuration changes) and remediate any identified artifacts.
  - Review the impacted `user.id` for compromise, revoke active sessions as appropriate, and reset credentials based on your incident response policy.
  - Use extracted indicators and distinctive script fragments to hunt for additional affected hosts and users.

- If the activity is verified benign:
  - Document the legitimate script source, expected `file.path` / `file.name`, and the normal execution context (`user.id`, `host.id`) to speed up future triage.
  - Monitor for deviations in execution context or significant changes in obfuscation metrics (for example, increased `Esql.script_block_pattern_count` or higher entropy) that could indicate abuse of an otherwise legitimate script.

