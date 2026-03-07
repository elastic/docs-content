---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential PowerShell Obfuscation via Invalid Escape Sequences" prebuilt detection rule.
---

# Potential PowerShell Obfuscation via Invalid Escape Sequences

## Triage and analysis

> **Disclaimer**:
> This guide was created by humans with the assistance of generative AI. While its contents have been manually curated to include the most valuable information, always validate assumptions and adjust procedures to match your internal runbooks and incident triage and response policies.

### Investigating Potential PowerShell Obfuscation via Invalid Escape Sequences

This rule flags PowerShell script block content that repeatedly inserts invalid backtick escape sequences within otherwise contiguous word characters. This can fragment tokens (cmdlets, parameters, variable names, strings) while preserving execution and readability to the interpreter, which can hinder content inspection and pattern-based detections.

Analyst goals:
- Reconstruct complete script block content when split across multiple events.
- Normalize the content (remove or correct invalid escapes) to reveal the underlying logic.
- Determine execution context (host, user, script origin) and correlate with adjacent activity to assess intent and impact.

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

- Establish timeline and ownership:
  - Anchor the activity using `@timestamp`, then record `host.name`, `host.id`, and `agent.id`.
  - Identify the execution context with `user.name`, `user.domain`, and `user.id`. Note whether the account is expected to run PowerShell on this host and whether the host is commonly used for scripting.

- Assess the likelihood of intentional obfuscation:
  - Review `Esql.script_block_pattern_count` to understand how heavily the content is fragmented. Higher counts generally increase confidence that this is deliberate obfuscation rather than incidental escaping.
  - Use `powershell.file.script_block_length` as size context and review `powershell.file.script_block_entropy_bits`, `powershell.file.script_block_unique_symbols`, and `powershell.file.script_block_surprisal_stdev` to characterize the content (simple text vs. mixed/randomized payloads).
  - Compare `Esql.script_block_tmp` to `powershell.file.script_block_text` to understand where obfuscation is concentrated (localized string vs. widespread token fragmentation).

- Reconstruct complete content when split across events:
  - If `powershell.total` is greater than 1, pivot on `powershell.file.script_block_id` and rebuild the script by ordering segments on `powershell.sequence`.
  - Validate the reconstructed set is complete (sequence 1 through `powershell.total`). Missing segments should be treated as an investigative gap and may require additional scoping.

- Determine script origin and delivery:
  - If `file.path`, `file.directory`, and `file.name` are present, treat the script block as file-associated. Evaluate whether the location and naming are consistent with approved scripts or expected tooling for the endpoint.
  - If file fields are absent, treat the script as inline or dynamically generated content and prioritize correlation by `host.id`, `user.id`, and time.

- Normalize and interpret the script content safely:
  - In a controlled analysis workflow, normalize the script by removing or correcting invalid backtick insertions so that split tokens become readable. Keep both the original and normalized versions for reporting.
  - Review the normalized text for behaviors that indicate malicious intent (secondary payload retrieval, dynamic execution, decoding/decompression, data collection, persistence logic, or remote interaction).
  - Extract and document indicators present in the content (network destinations, file paths/names, unique strings, or embedded encoded blobs) for scoping.

- Correlate within PowerShell telemetry:
  - Pivot on `host.id` and `user.id` to identify additional `powershell.file.script_block_text` events shortly before and after the alert time to capture staging, follow-on commands, and potential cleanup.
  - Check for the same `powershell.file.script_block_id` appearing across hosts, or for repeated normalized strings, to identify automation reuse or broader activity.

- Correlate with adjacent endpoint activity (if available in your environment):
  - Review process execution around `@timestamp` on `host.name` to identify the PowerShell host process and its parent, then assess whether the launch chain aligns with expected activity for the user and endpoint.
  - Review network activity around the alert time for connections that align with indicators extracted from the script content.
  - Review file and registry activity around the same time window for artifacts consistent with the script (new or modified scripts, dropped files, or persistence-related changes).
  - Review authentication activity associated with `user.id` around the alert time for suspicious logons or remote access that may align with script execution.

- Scope impact:
  - Search for other alerts/events with similar obfuscation characteristics on the same host and for the same user to determine whether this is a one-off execution or a repeated pattern.
  - If multiple hosts are involved, prioritize investigation for critical assets and accounts with elevated privileges.

### False positive analysis

- Legitimate scripts can contain backticks for formatting, string construction, or content generation; however, repeated invalid escape sequences embedded inside alphanumeric tokens are uncommon. Validate whether the execution context (`host.id`, `user.id`) aligns with known administrative or developer activity.
- Some commercial or internal tools intentionally obfuscate PowerShell to protect intellectual property. Confirm whether the script origin (`file.path` when present), account context, and prevalence across the environment match an approved application or workflow.
- Copy/paste artifacts and encoding transformations can introduce unexpected characters. When suspected, compare the normalized content to known-good scripts and assess whether the obfuscation is systematic (repeating across many tokens) versus localized.

### Response and remediation

- If the activity is confirmed or strongly suspected malicious:
  - Contain affected host(s) to prevent further execution and lateral movement.
  - Preserve evidence: reconstructed `powershell.file.script_block_text`, `powershell.file.script_block_id`, `powershell.sequence`, `powershell.total`, and alert-derived fields (`Esql.script_block_tmp`, `Esql.script_block_pattern_count`, and the script block metrics).
  - If `file.path` is present, collect and quarantine the referenced script and review the surrounding directory for related artifacts.
  - Use indicators extracted from normalized content to scope related activity across endpoints (pivot on `host.id`, `user.id`, `file.path`, and unique strings from the script).
  - Coordinate credential remediation for affected accounts when remote execution, credential material, or post-exploitation behavior is suspected.

- If the activity is benign but requires reduction:
  - Document the legitimate source (expected hosts/users and `file.path` when applicable).
  - Apply narrowly scoped tuning using stable attributes available in the alert (such as `host.id`, `user.id`, and `file.path`) and continue monitoring for deviations in script content and execution context.

