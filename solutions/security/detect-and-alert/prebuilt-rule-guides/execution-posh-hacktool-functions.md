---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential PowerShell HackTool Script by Function Names" prebuilt detection rule.
---

# Potential PowerShell HackTool Script by Function Names

## Triage and analysis

> **Disclaimer**:
> This guide was created by humans with the assistance of generative AI. While its contents have been manually curated to include the most valuable information, always validate assumptions and adjust procedures to match your internal runbooks and incident triage and response policies.

### Investigating Potential PowerShell HackTool Script by Function Names

This rule identifies PowerShell Script Block Logging events where the captured script content includes function names commonly reused by offensive PowerShell toolkits. Script blocks can contain function definitions (tool staging) and/or function invocation (active use). Prioritize determining what capability is present, how the script was introduced, and whether follow-on activity occurred.

#### Key alert fields to review

- `user.name`, `user.domain`, `user.id`: Account execution context for correlation, prioritization, and scoping.
- `host.name`, `host.id`: Host execution context for correlation, prioritization, and scoping.
- `powershell.file.script_block_text`: Script block content that matched the detection logic.
- `powershell.file.script_block_id`, `powershell.sequence`, `powershell.total`: Script block metadata to pivot to other fragments or reconstruct full script content when split across multiple events.
- `file.path`, `file.directory`, `file.name`: File-origin context when the script block is sourced from an on-disk file.
- `powershell.file.script_block_length`: Script block length (size) context.

#### Possible investigation steps

- Review `powershell.file.script_block_text` to determine intent and urgency:
  - Identify the function name(s) present and map them to likely capability. Examples include:
    - Credential access: `Invoke-Mimikatz`, `Invoke-Kerberoast`, `Invoke-DCSync`, `Get-GPPPassword`, `Get-LSASecret`.
    - Injection or token manipulation: `Invoke-ReflectivePEInjection`, `Create-RemoteThread`, `Inject-RemoteShellcode`, `Invoke-TokenManipulation`.
    - Remote execution or lateral movement: `Invoke-PsExec`, `Invoke-SMBExec`, `Invoke-WmiCommand`, `Invoke-PSRemoting`, `Invoke-DCOM`.
    - Staging, persistence, or exfiltration: `Invoke-DownloadCradle`, `Add-Persistence`, `HTTP-Backdoor`, `Do-Exfiltration`.
  - Determine whether the script block primarily defines functions (tool staging) or calls them (active use). If only definitions are present, look for follow-on script blocks from the same host and user that invoke the functions.
  - Capture any embedded targets or indicators visible in the text (other usernames, hostnames, domains, remote paths, URLs, or IP addresses).

- Reconstruct the complete script when it is split across multiple events:
  - Pivot using `host.name` (or `host.id`) and `powershell.file.script_block_id` to collect related script blocks around `@timestamp`.
  - Order fragments using `powershell.sequence` and confirm completeness using `powershell.total`.
  - Use `powershell.file.script_block_length` as a size signal to distinguish a full toolkit/module from a small launcher or single command.

- Establish script origin and execution context:
  - If `file.path` / `file.name` (and `file.directory`) are present, treat the script as an on-disk artifact. Validate whether its location and naming align with approved scripts and expected administrative workflows for that host and user.
  - If file fields are not present, treat the activity as potentially interactive or in-memory. Correlate other endpoint telemetry from the same `host.id` and time window to identify how PowerShell was started and what else executed immediately before and after.

- Validate the account and host context:
  - Review `user.name`, `user.domain`, and `user.id` for privilege level and whether the activity aligns with expected responsibilities and working hours.
  - Review `host.name` and `host.id` to understand the system role and whether advanced PowerShell activity is expected on that host.

- Scope for additional related activity on the same host:
  - Search for other script blocks on the same `host.id` and `user.id` near the alert time to identify staging, follow-on commands, or cleanup actions.
  - Pivot on `powershell.file.script_block_id` to ensure all fragments are reviewed and to detect repeated execution of the same script content.

- Scope for related activity across the environment:
  - Search for additional script blocks containing the same distinctive function name(s) or matching snippets of `powershell.file.script_block_text` to identify reuse and potential spread.
  - If `file.path` or `file.name` is present, check for the same script artifact referenced on other hosts.

- Correlate with adjacent telemetry (as available) to confirm impact and intent:
  - Process telemetry to identify the initiating process (parent of PowerShell) and any suspicious child processes spawned after the script executed.
  - Authentication telemetry to identify anomalous logons or access patterns involving the same user around the execution window.
  - Network and DNS telemetry to identify outbound connections, internal scanning, or remote management activity aligned with `@timestamp`.
  - Persistence telemetry to identify new or modified services, scheduled tasks, autoruns, or registry changes that align with the observed script capability.

### False positive analysis

- Internal security or IT teams may run proof-of-concept or validation scripts for training, detection testing, or incident response. Confirm script ownership, change control, and expected distribution.

### Response and remediation

- If the activity is unauthorized or suspicious:
  - Contain the affected host to prevent additional execution and lateral movement.
  - Preserve evidence by saving all related script block events (reconstruct full content using `powershell.file.script_block_id`, `powershell.sequence`, and `powershell.total`) and collecting any referenced on-disk script identified by `file.path`.
  - Prioritize impact assessment based on the functions observed (credential access, injection, remote execution, persistence, or exfiltration) and look for corroborating activity in adjacent telemetry.
  - Scope for additional impacted systems and accounts by searching for the same function names or script snippets across other hosts and users.
  - Remove identified artifacts and persistence mechanisms, and monitor for re-execution using the same function-name patterns.

- If the activity is confirmed benign:
  - Document the justification (owner, purpose, expected hosts/users, and time window) and retain the reconstructed script content for future baselining.
  - Where feasible, limit high-risk PowerShell tooling to controlled administrative hosts and approved accounts to reduce recurrence.

