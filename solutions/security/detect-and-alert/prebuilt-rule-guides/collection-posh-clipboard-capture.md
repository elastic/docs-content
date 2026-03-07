---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "PowerShell Suspicious Script with Clipboard Retrieval Capabilities" prebuilt detection rule.'
---

# PowerShell Suspicious Script with Clipboard Retrieval Capabilities

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating PowerShell Suspicious Script with Clipboard Retrieval Capabilities

This alert indicates PowerShell script block content associated with clipboard access. The matched script may use the Get-Clipboard cmdlet or Windows clipboard APIs (for example, Windows.Forms.Clipboard or related UI components) to retrieve user-copied data. Clipboard collection is often opportunistic and may be used to capture credentials, tokens, and other sensitive information copied during normal workflows.

#### Key alert fields to review

- `user.name`, `user.domain`, `user.id`: Account execution context for correlation, prioritization, and scoping.
- `host.name`, `host.id`: Host execution context for correlation, prioritization, and scoping.
- `powershell.file.script_block_text`: Script block content that matched the detection logic.
- `powershell.file.script_block_id`, `powershell.sequence`, `powershell.total`: Script block metadata to pivot to other fragments or reconstruct full script content when split across multiple events.
- `file.path`, `file.directory`, `file.name`: File-origin context when the script block is sourced from an on-disk file.
- `powershell.file.script_block_length`: Script block length (size) context.

#### Possible investigation steps

- Review `powershell.file.script_block_text` to understand the clipboard access technique and usage pattern:
  - Get-Clipboard usage versus .NET/UI based access (for example, Windows.Forms.Clipboard, Windows.Clipboard, TextBox.Paste, or methods such as GetText).
  - Whether clipboard access appears to be a one-time action or part of repeated/polled collection logic (for example, loops, timers, or repeated calls in the same script).
- Reconstruct the complete script when content is split across multiple events:
  - Pivot on `powershell.file.script_block_id` and order related events by `powershell.sequence` to rebuild the full script up to `powershell.total`.
  - Use `powershell.file.script_block_length` as context for unusually large scripts, which may indicate additional functionality beyond clipboard retrieval.
- Evaluate intent by reviewing surrounding logic in `powershell.file.script_block_text`:
  - Where clipboard contents are stored (variables, arrays, buffers) and whether the script transforms data after retrieval (for example, encoding, compression, string manipulation, or obfuscation).
  - Any indications of staging or transfer behavior following clipboard access (for example, writing data to disk or preparing network requests).
- Validate provenance and expected use:
  - Use `user.name`, `user.domain`, and `user.id` to determine whether the execution context is expected to run PowerShell that interacts with the clipboard.
  - Use `host.name` and `host.id` to determine whether the affected host is a typical endpoint for interactive clipboard use or an unusual target for clipboard collection.
  - If `file.path`, `file.directory`, or `file.name` are present, assess whether the script source is expected for the user and host, and whether it is located in a user-writable or temporary location.
- Determine execution context and whether the activity is user-driven or automated:
  - Correlate activity for the same `host.id` and `user.id` with process execution telemetry (if available) to identify the PowerShell host and its parent process, and whether execution was interactive or automated.
  - If authentication telemetry is available, correlate nearby logon activity for the same user and host to identify newly established sessions or unusual remote access preceding the alert.
- Scope and prevalence:
  - Search for other script block events with similar clipboard-related strings in `powershell.file.script_block_text` for the same `user.id` and `host.id`, and then across other hosts to identify reuse.
  - Look for reuse of the same `file.name` or `file.path` across hosts, which can indicate shared tooling or broader distribution.
- Assess impact and potential exposure:
  - If the script suggests repeated clipboard reads or immediate staging/transfer behavior, treat clipboard contents handled by the affected user on the host during the timeframe as potentially exposed and prioritize investigation accordingly.

### False positive analysis

- Clipboard retrieval can be legitimate in user productivity scripts, developer/test utilities, and administrative automation that transforms or inserts copied content into other workflows.
- Benign activity is more likely when the script source (`file.path`/`file.name`) aligns with known internal tooling, the user context is expected, and the script block text shows clear user-facing intent without follow-on staging or transfer behavior.
- False positives are less likely when clipboard access is repeated or automated, appears on atypical hosts for interactive use, or is coupled with suspicious handling of the retrieved data (for example, encoding, buffering, or writing to unexpected locations).

### Response and remediation

- If the activity is confirmed benign, document the script, expected users/hosts, and the business justification. Ensure the script source is maintained under change control to detect unauthorized modifications.
- If suspicious or malicious activity is suspected:
  - Contain the affected host to prevent further collection and preserve evidence.
  - Preserve relevant artifacts, including all related script block events for the `powershell.file.script_block_id` and any referenced script file from `file.path` (if present).
  - Investigate for downstream handling of clipboard data (staging or transfer) using available endpoint, file, network, and authentication telemetry scoped to `host.id` and `user.id`.
  - Assess potential credential or token exposure for the affected user and initiate credential hygiene actions appropriate to your environment.
  - Remove or remediate the execution source (malicious scripts or unauthorized automation) and investigate for persistence mechanisms that could re-run the clipboard collection.
  - Expand scoping by hunting for the same clipboard retrieval patterns in `powershell.file.script_block_text`, and for reuse of the same `file.name`/`file.path` across other hosts.
  - Capture lessons learned and update monitoring and access controls to reduce future abuse of PowerShell-based collection techniques while preserving required operational use cases.
