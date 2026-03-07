---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential PowerShell Obfuscation via High Numeric Character Proportion" prebuilt detection rule.
---

# Potential PowerShell Obfuscation via High Numeric Character Proportion

## Triage and analysis

> **Disclaimer**:
> This guide was created by humans with the assistance of generative AI. While its contents have been manually curated to include the most valuable information, always validate assumptions and adjust procedures to match your internal runbooks and incident triage and response policies.

### Investigating Potential PowerShell Obfuscation via High Numeric Character Proportion

This rule flags long PowerShell script blocks with unusually digit-dense content. Numeric-heavy script blocks are often used to conceal payloads as byte arrays or character codes that are decoded at runtime. Triage should focus on reconstructing the full script content, determining how it was initiated, and identifying any decoded or executed secondary content.

#### Key alert fields to review

- `user.name`, `user.domain`, `user.id`: Account execution context for correlation, prioritization, and scoping.
- `host.name`, `host.id`: Host execution context for correlation, prioritization, and scoping.
- `file.path`, `file.directory`, `file.name`: File-origin context when the script block is sourced from an on-disk file.
- `powershell.file.script_block_text`: Script block content that matched the detection logic.
- `powershell.file.script_block_id`, `powershell.sequence`, `powershell.total`: Script block metadata to pivot to other fragments or reconstruct full script content when split across multiple events.
- `Esql.script_block_tmp`: Transformed script block where detection patterns replace original content with a marker to support scoring/counting and quickly spot match locations.
- `Esql.script_block_ratio`: Proportion of the script block's characters that match the alert's target character set, divided by total script length (0-1).
- `Esql.script_block_pattern_count`: Count of matches for the detection pattern(s) observed in the script block content.
- `powershell.file.script_block_entropy_bits`: Shannon entropy of the script block. Higher values may indicate obfuscation.
- `powershell.file.script_block_surprisal_stdev`: Standard deviation of surprisal across the script block. Low values indicate uniform randomness. High values indicate mixed patterns and variability.
- `powershell.file.script_block_unique_symbols`: Count of distinct characters present in the script block.
- `powershell.file.script_block_length`: Script block length (size) context.

#### Possible investigation steps

- Review `powershell.file.script_block_text` to characterize the numeric content:
  - Look for long comma-separated numbers, repeated digit sequences, or `0x`-prefixed values that may represent reconstructed bytes.
  - Identify string reconstruction patterns (for example, casting numeric values to characters) and any subsequent decoding or decompression logic.
  - Note any execution primitives that would run derived content (for example, invoking dynamically built commands or loading content into memory).
- If the script is fragmented, use `powershell.sequence` and `powershell.total` to collect the related script block events on the same `host.name` and `user.id` and reconstruct the complete content in the correct order before drawing conclusions.
- Establish execution context and scope using `host.name`, `host.id`, `agent.id`, and `user.id`:
  - Determine whether the user context is expected to run PowerShell and whether similar script blocks have occurred recently on the same host or by the same user.
  - Look for other alerts on the same host or user that could indicate staging, persistence, or lateral movement.
- Assess script origin using `file.path` and `file.directory` when present:
  - Determine whether the script is sourced from a location consistent with approved administration or automation workflows.
  - If the script is file-backed, check for other security telemetry referencing the same path to identify file creation, modification, or repeated execution patterns.
- Correlate with adjacent telemetry (as available in your environment) using the host and user pivots above:
  - Process execution telemetry near the alert time to identify the PowerShell host process and its parent, and to understand how PowerShell was launched.
  - Network telemetry for outbound connections or downloads that could support payload retrieval or command and control.
  - File activity for dropped payloads or staging artifacts related to the script content or its on-disk source.

### False positive analysis

- Legitimate scripts that embed binary content as numeric arrays (for example, packaging resources into scripts or deploying configuration blobs) can appear digit-dense.
- Administrative tooling that generates large reports, inventories, or exports may include extensive numeric identifiers and constants.
- Some legitimate security or management products may produce numeric-heavy PowerShell content as part of automation; validate against known software, expected execution accounts, and change windows.

### Response and remediation

- If malicious behavior is suspected, contain the affected host to prevent further execution and reduce the risk of follow-on activity.
- Preserve the script content from `powershell.file.script_block_text` (and any reconstructed multi-part content) for deeper analysis and to support incident response and retrospective hunting.
- If `file.path` is present and the source is not authorized, remove or quarantine the script and investigate related host artifacts and execution mechanisms.
- Investigate potential account compromise for the associated `user.id` by reviewing recent authentication and endpoint activity; take credential and session remediation actions in line with your procedures.
- Hunt for related activity using `host.id`, `agent.id`, `user.id`, and distinctive script patterns identified during triage to find additional impacted systems.
- Apply preventive controls based on findings, such as tightening PowerShell usage for affected accounts, improving script provenance controls, and enhancing monitoring for similar obfuscation patterns.

