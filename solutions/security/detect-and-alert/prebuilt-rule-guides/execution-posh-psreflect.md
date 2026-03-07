---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "PowerShell PSReflect Script" prebuilt detection rule.
---

# PowerShell PSReflect Script

## Triage and analysis

> **Disclaimer**:
> This guide was created by humans with the assistance of generative AI. While its contents have been manually curated to include the most valuable information, always validate assumptions and adjust procedures to match your internal runbooks and incident triage and response policies.

### Investigating PowerShell PSReflect Script

This rule detects PowerShell scripts consistent with PSReflect-style helpers used to dynamically define in-memory .NET types and invoke Win32 APIs via interop (for example, Add-Win32Type, New-InMemoryModule, and DllImport patterns). This technique can be used for legitimate administration and development, but it is also commonly used by adversaries to access native capabilities from PowerShell.

#### Key alert fields to review

- `user.name`, `user.domain`, `user.id`: Account execution context for correlation, prioritization, and scoping.
- `host.name`, `host.id`: Host execution context for correlation, prioritization, and scoping.
- `powershell.file.script_block_text`: Script block content that matched the detection logic.
- `powershell.file.script_block_id`, `powershell.sequence`, `powershell.total`: Script block metadata to pivot to other fragments or reconstruct full script content when split across multiple events.
- `file.path`, `file.directory`, `file.name`: File-origin context when the script block is sourced from an on-disk file.
- `powershell.file.script_block_length`: Script block length (size) context.

#### Possible investigation steps

- Review the alert context to prioritize the investigation:
  - Identify the affected host (`host.name`, `host.id`) and the execution context (`user.name`, `user.domain`, `user.id`).
  - Use `@timestamp` to scope a short timeline around the activity and identify related alerts on the same host or user.
  - Treat activity as higher risk when the executing account is unexpected for PowerShell development/administration or when the host is not typically used for scripting.

- Reconstruct the complete script block content before assessing intent:
  - Pivot on `powershell.file.script_block_id` to locate all related events.
  - Order events by `powershell.sequence` and confirm whether the observed sequence aligns with `powershell.total`.
  - Combine the fragments into a single script view to avoid misinterpreting partial content.

- Analyze `powershell.file.script_block_text` to understand capability and likely intent:
  - Identify which PSReflect artifacts are present (for example, `Add-Win32Type`, `New-InMemoryModule`, `psenum`, `DefineDynamicAssembly`, `DefineDynamicModule`, and `Runtime.InteropServices.DllImportAttribute`).
  - Determine whether the content is primarily a helper library (type/struct/enum definitions and import scaffolding) or includes immediate API calls or operational logic.
  - If `DllImportAttribute` is used, extract the referenced DLLs and imported function names from the script text and map them to likely objectives (for example, process/memory operations, token and privilege manipulation, registry or service interaction, or networking).
  - Capture distinctive identifiers from the script (function names, type names, imported API names, unique strings) to support scoping and hunting.

- Establish script origin and distribution:
  - If `file.path`/`file.name` are present, treat the script as file-backed and assess whether the location and filename align with approved tooling and change control.
  - If `file.path` is not present, consider that the script may have been executed interactively or delivered in-memory, and prioritize correlation with surrounding activity for the same `user.id` and `host.id`.

- Scope the activity across time, hosts, and users:
  - Search for additional script blocks on the same `host.id` and `user.id` around `@timestamp` to identify preceding staging activity and follow-on behavior.
  - Hunt across the environment for the same `file.path`/`file.name` and for distinctive strings extracted from `powershell.file.script_block_text` to identify other impacted hosts.
  - Pivot on `user.id` to determine whether the same account executed similar PSReflect content on other endpoints.

- Correlate with adjacent telemetry (if available) to confirm execution chain and impact:
  - Process telemetry: identify the PowerShell host process and its parent process to understand how the script was initiated (interactive, automated, or remote execution context).
  - Network telemetry: review DNS lookups and outbound connections near the alert time for evidence of staging, command-and-control, or lateral movement.
  - Endpoint changes: review file, service, scheduled task, and registry activity after the script execution to identify persistence, payload delivery, or privilege changes that align with the capabilities implied by the script text.
  - If Elastic Osquery response actions are available, collect DNS cache and service inventory to support scoping and to identify suspicious services or unsigned service binaries.

### False positive analysis

- False positives are possible in environments where administrators, developers, or internal tooling use PSReflect-style code to access native APIs from PowerShell.
- Validate legitimacy by confirming that:
  - The executing account and host are expected to run advanced PowerShell code (`user.id`, `user.name`, `host.id`, `host.name`).
  - The script source is known and controlled when `file.path`/`file.name` are present (for example, approved repositories, deployment paths, or administrative script locations).
  - The script content and its imported APIs are consistent with a documented operational need and do not align with common attacker objectives (for example, credential access, injection, or persistence).
- If the activity is recurring, baseline expected frequency and approved users/hosts to distinguish routine usage from anomalous execution.

### Response and remediation

- If malicious activity is confirmed or suspected:
  - Contain the affected host to prevent further execution and lateral movement, following your incident response procedures.
  - Preserve evidence: the fully reconstructed script (`powershell.file.script_block_id` with `powershell.sequence`/`powershell.total`), the raw script content (`powershell.file.script_block_text`), and any referenced file path details (`file.path`, `file.name`).
  - Use extracted identifiers (imported API names, helper function names, unique strings) to hunt for related activity across other hosts and users.
  - Investigate and remediate follow-on activity identified during correlation (persistence mechanisms, suspicious services, unexpected outbound connections, and any dropped or modified files).
  - If account compromise is suspected, reset credentials for the impacted user and review recent authentication activity to identify additional compromised assets.

- If the activity is confirmed benign:
  - Document the legitimate script/tool, expected hosts/users, and the operational purpose to speed up future triage.
  - Where appropriate, improve controls around advanced PowerShell usage (least privilege for scripting accounts, controlled script distribution, code review, and continued logging coverage).

