---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "PowerShell Obfuscation via Negative Index String Reversal" prebuilt detection rule.
---

# PowerShell Obfuscation via Negative Index String Reversal

## Triage and analysis

> **Disclaimer**:
> This guide was created by humans with the assistance of generative AI. While its contents have been manually curated to include the most valuable information, always validate assumptions and adjust procedures to match your internal runbooks and incident triage and response policies.

### Investigating PowerShell Obfuscation via Negative Index String Reversal

This alert flags PowerShell script block content that uses negative index ranges to reverse strings or arrays and rebuild content at runtime. This pattern can be used to hide command text and reduce readability during review, so the primary goal is to recover the reconstructed content and determine what it does in the observed execution context.

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

- Review `powershell.file.script_block_text` and locate the reversal logic. Use `Esql.script_block_tmp` to quickly find match positions, then identify:
  - The variable or array being reversed
  - The reconstructed output (string, byte array, or command fragment)
  - The sink where the output is used (for example, passed into a dynamic execution routine, used as a URL, or written to disk)
- Reconstruct the final value produced by the reversal. Focus on what the script is trying to rebuild (commands, URLs, file paths, registry paths, encoded blobs, or arguments) and record the recovered strings for scoping.
- If the script block is fragmented, pivot on `powershell.file.script_block_id` and use `powershell.sequence` and `powershell.total` to rebuild the full script in order. Reassess intent based on the complete content rather than a single fragment.
- Use `Esql.script_block_pattern_count` to prioritize reviews:
  - Single-use reversal may be utility logic and requires context to judge
  - Repeated reversal across a long script is more consistent with obfuscation wrappers
- Use script complexity signals to guide triage:
  - High `powershell.file.script_block_entropy_bits` and high `powershell.file.script_block_unique_symbols` can indicate encoded or staged content
  - Compare `powershell.file.script_block_surprisal_stdev` with the script content to determine whether the script mixes readable logic with high-randomness segments
- Validate execution context with `user.name`, `user.domain`, `user.id`, `host.name`, and `host.id`. Prioritize investigation when the user is unexpected for the host, the host is sensitive, or similar activity is new for that account.
- Review `file.path`, `file.directory`, and `file.name` (if present) to understand script origin. Treat unknown locations, new or renamed scripts, and ambiguous naming as higher risk, and check for additional script blocks tied to the same path.
- Scope related activity by searching for additional PowerShell script block events on the same `host.id` and `user.id` around `@timestamp`, and by pivoting on the same `powershell.file.script_block_id`. Look for:
  - Follow-on script blocks with clearer (deobfuscated) commands
  - Repeated use of similar reversal segments or reconstructed indicators
- If other endpoint telemetry is available, correlate activity on the same host and time window to identify what happened next (process launches, network connections, file writes, or other changes) and validate whether outcomes align with the reconstructed content.

### False positive analysis

- Legitimate scripts may reverse arrays or strings for formatting, parsing, or testing. These cases typically remain readable end-to-end and do not rely on multiple layers of reconstruction to produce executable behavior.
- Developer utilities and automation tooling can include dense string manipulation. Validate whether the observed `file.path` and execution context (`user.name`, `host.name`) align with approved workflows and whether the same script content recurs consistently across expected hosts.
- If activity is confirmed benign, prefer context-based tuning using stable attributes visible in the alert (for example, consistent `file.path` and recognizable script content patterns) rather than suppressing the technique broadly.

### Response and remediation

- If the reconstructed content indicates malicious behavior, isolate the affected host to limit further execution and reduce the risk of lateral movement.
- Preserve evidence by retaining the full `powershell.file.script_block_text` and all related fragments grouped by `powershell.file.script_block_id`. Capture the reconstructed strings and relevant metadata (`powershell.sequence`, `powershell.total`, `Esql.script_block_pattern_count`) in case notes.
- Identify and contain the execution source. If an unauthorized on-disk script is referenced by `file.path`, remove or quarantine it and investigate how it was introduced using your standard incident response workflow.
- Investigate the associated account (`user.id`) for signs of compromise. Apply account controls (credential reset, session invalidation, privilege review) based on your procedures and observed scope.
- Hunt for additional exposure by pivoting on recovered indicators and on recurrence of the reversal technique across hosts and users. Remediate any additional impacted endpoints identified during scoping.
- After containment, improve preventative controls appropriate for your environment, such as restricting PowerShell usage to approved users/hosts and enhancing monitoring for obfuscation and dynamic execution patterns.

