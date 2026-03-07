---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential PowerShell Obfuscation via High Special Character Proportion" prebuilt detection rule.
---

# Potential PowerShell Obfuscation via High Special Character Proportion

## Triage and analysis

> **Disclaimer**:
> This guide was created by humans with the assistance of generative AI. While its contents have been manually curated to include the most valuable information, always validate assumptions and adjust procedures to match your internal runbooks and incident triage and response policies.

### Investigating Potential PowerShell Obfuscation via High Special Character Proportion

This rule alerts on PowerShell Script Block Logging content where non-alphanumeric characters make up an unusually large share of the script text. This pattern is frequently produced by encoding, aggressive escaping, string mangling, or dynamic code generation intended to hinder inspection.

The alert includes scoring and script-shape fields that help distinguish benign embedded data from suspicious deobfuscation/execution logic. Treat the script block text as potentially untrusted content and focus on reconstructing the full script and identifying downstream behavior through correlation.

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

- Establish scope and execution context:
  - Review `@timestamp` to set an investigation window and identify preceding/follow-on activity.
  - Identify the affected `host.id`/`host.name` and the executing `user.id`/`user.name`/`user.domain`.
  - Determine whether the user/host pairing is expected for PowerShell usage in your environment and whether the account is privileged or widely used.

- Interpret the alert scoring and "shape" signals:
  - Review `Esql.script_block_ratio` and `Esql.script_block_pattern_count` alongside `powershell.file.script_block_length` to understand how extreme the special-character density is.
  - Use `Esql.script_block_tmp` to quickly assess whether the special characters cluster in a single region (for example, one embedded blob) or are distributed throughout the script (for example, pervasive mangling).
  - Use `powershell.file.script_block_entropy_bits`, `powershell.file.script_block_unique_symbols`, and `powershell.file.script_block_surprisal_stdev` to guide prioritization:
    - High entropy with many unique symbols commonly aligns with encoded/compressed/encrypted blobs embedded in the script.
    - High special-character ratio with lower entropy can align with heavy escaping, string concatenation, or code generation.
    - Low surprisal variability (low standard deviation) can indicate uniformly random-looking content typical of dense encoding.

- Reconstruct the full script block before making a determination:
  - Pivot on `powershell.file.script_block_id` to collect all fragments for the script block.
  - Reassemble fragments in order using `powershell.sequence` and confirm completeness using `powershell.total`.
  - If fragments are missing, treat the visible content as incomplete and continue collection/scoping before concluding intent.

- Analyze `powershell.file.script_block_text` for intent and technique:
  - Identify whether the content is primarily data (for example, long opaque strings) or executable logic (functions, control flow, and invocation).
  - Look for common deobfuscation and dynamic execution patterns, such as:
    - Decoding/decompression routines (for example, Base64 decoding, byte/char transformations, compression streams).
    - Dynamic invocation or staged execution (for example, `Invoke-Expression`/`IEX`, reflection, `.Invoke()`, `Add-Type`).
    - Retrieval of remote content or secondary payloads (for example, web request/client usage, download-and-execute flow).
  - If the script includes clear indicators (domains, URLs, IP addresses, file paths, file names), capture them from the script text for pivoting and scoping.

- Determine provenance and expectedness using available file context:
  - If `file.path`/`file.directory`/`file.name` are present, assess whether the location and naming align with known administrative scripts or approved automation.
  - If file fields are absent, treat the activity as potentially interactive or in-memory and prioritize identifying what initiated PowerShell through adjacent host telemetry.

- Correlate with adjacent telemetry (as available in your environment) to confirm impact:
  - Process activity on the same host and time window to determine the initiating process and whether PowerShell was launched indirectly.
  - Network activity to identify outbound connections consistent with download, staging, or command-and-control behavior.
  - File and registry activity to identify dropped artifacts or persistence-related changes.
  - Authentication activity for the same `user.id` to identify suspicious logons or lateral movement preceding the script execution.

- Expand scope across the environment:
  - Search for additional script block events on the same `host.id` and `user.id` near the alert time to identify staged execution (for example, decoding in one block, execution in another).
  - Hunt for similar script content using stable substrings from `powershell.file.script_block_text`, and group by `file.name` or `file.path` when present to identify reuse.

### False positive analysis

- False positives are most likely when scripts embed or manipulate large non-code payloads (for example, serialized objects, structured data, certificates, or compressed content) or when tooling auto-generates scripts with heavy escaping and templating.
- Validate benign hypotheses by confirming a consistent execution pattern over time (recurring `host.id` and `user.id`), expected provenance (`file.path`/`file.name` when present), and script content that performs known administrative functions rather than decoding and executing newly generated code.
- Treat unexpected execution context (new user/host pairing) combined with high entropy and opaque content as higher risk, even if the script text does not immediately reveal its final payload.

### Response and remediation

- If malicious or suspicious activity is confirmed:
  - Contain the affected host to prevent additional execution and lateral movement.
  - Preserve evidence from the alert, including `powershell.file.script_block_text`, reconstructed fragments (if applicable), `powershell.file.script_block_id`, and the scoring fields (`Esql.script_block_ratio`, `Esql.script_block_pattern_count`, `powershell.file.script_block_entropy_bits`).
  - Identify and remediate follow-on behavior discovered during correlation (downloaded payloads, dropped files, persistence changes, or suspicious network destinations).
  - Scope the intrusion by searching for similar script content across the environment using stable substrings from `powershell.file.script_block_text`, and by pivoting on `user.id`, `host.id`, `file.path`, and `file.name`.
  - If account compromise is suspected, reset credentials for the affected user and review other recent activity for that `user.id`.

- If the activity is determined benign:
  - Document the responsible script or workflow, expected execution context, and typical frequency.
  - Monitor for deviations such as new hosts, new users, or materially different script content that may indicate abuse of a legitimate mechanism.

