---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Command Prompt Network Connection" prebuilt detection rule.
---

# Suspicious Command Prompt Network Connection

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Command Prompt Network Connection

This alert identifies a Windows `cmd.exe` process start event that is quickly followed by a network connection from the same `cmd.exe` instance (`process.entity_id`). The command line indicates scripted execution (batch files), references to remote resources (URL-like strings), or execution launched by a Microsoft Office application. This pattern can be used to download payloads, stage execution, or establish command and control.

#### Triage and analysis steps

- Confirm the matched sequence and keep analysis tied to the correct process instance:
  - Use the `Investigate in timeline` button in the Alerts table or pivot on `process.entity_id` to review both the process start event and the associated network event(s).
  - Example KQL pivots:
    - `process.entity_id:"<process_entity_id>" and event.category:process`
    - `process.entity_id:"<process_entity_id>" and event.category:network`

- Determine why `cmd.exe` matched and assess intent:
  - Review `process.args` to confirm the interpreter switch (`/c` to execute and exit, `/k` to remain open).
  - Identify which match condition applies:
    - Batch script: `process.args` includes a `.bat` or `.cmd` reference.
    - Remote resource: `process.command_line` contains `http://`, `https://`, or `ftp://`.
    - Office parent: `process.parent.name` is one of `winword.exe`, `excel.exe`, `powerpnt.exe`, `outlook.exe`, `msaccess.exe`, or `mspub.exe`.
  - Look for staging or obfuscation patterns in `process.command_line` (for example: `&`/`&&`/`||`, pipes `|`, redirection `>`/`>>`, escaping `^`, environment variables, or long encoded strings).

- Validate the execution context and launch vector:
  - Review `user.*` fields to determine who ran the command and whether it is expected for the host role.
  - Review `process.parent.name` (and `process.parent.command_line` if available) to understand the initial trigger:
    - Office parent: prioritize identifying the initiating document or message and any user interaction around `@timestamp`.
    - Management tooling or installer parent: validate change control and whether the command line and destination are consistent with that software.
  - If a batch script is referenced, locate the script on the host (if telemetry allows) and capture path and hash (`file.path`, `file.hash.sha256`) for scoping.

- Analyze the outbound destination:
  - Review `destination.ip` and `destination.port` for expectedness (business relationship, known vendor, or organization-owned public IP space).
  - Note: the rule excludes common private and reserved address ranges, but it can still alert on connections to legitimate public services.
  - Pivot on `destination.ip` to identify other hosts contacting the same destination near `@timestamp`:
    - `destination.ip:"<destination_ip>" and event.category:network`
  - Check whether the same `process.entity_id` generated repeated connections (potential beaconing) versus a single connection (one-time retrieval).

- Reconstruct follow-on activity and potential impact:
  - Identify child processes spawned by `cmd.exe` and look for common follow-on tooling (for example: `powershell.exe`, `mshta.exe`, `rundll32.exe`, `regsvr32.exe`, `certutil.exe`, `bitsadmin.exe`, `curl.exe`, `wget.exe`).
  - If file telemetry is available, review file creation/modification shortly after `@timestamp` and correlate any new binaries or scripts with hashes and execution events.

- Scope the activity (blast radius):
  - Search for the same `process.command_line` (or distinctive substrings), script name, or extracted URL across endpoints.
  - Search for other `cmd.exe` instances connecting to the same `destination.ip` or the same destination port/protocol.
  - If the parent is Office, scope for the same parent-child relationship (`process.parent.name` -> `cmd.exe`) across users and hosts.

### False positive analysis

- Software deployment, packaging, or endpoint management workflows that use `cmd.exe /c` to run batch scripts and contact vendor services.
- Signed installer or updater activity where `cmd.exe` is used as a helper process with stable command lines.
- Documented Office macros/add-ins/templates that legitimately spawn `cmd.exe` with consistent command lines and destinations.

A benign determination is more likely when the combination of `process.parent.name`, stable `process.command_line`, and consistent `destination.ip`/`destination.port` repeats across an expected set of hosts and users and aligns to a documented workflow owner.

### Response and remediation

- If the activity is suspicious or cannot be attributed to an approved workflow:
  - Contain the affected endpoint (`host.id`) using available endpoint or network controls.
  - Preserve evidence (at minimum):
    - `@timestamp`, `host.*`, `user.*`
    - `process.entity_id`, `process.command_line`, `process.args`, `process.parent.*`
    - `destination.ip`, `destination.port`, `network.*`
    - Any related child processes and file artifacts (paths and hashes) identified during triage
  - Scope for related activity by searching for additional occurrences of the same destination and command-line patterns.
  - If Office is the launch vector, identify and quarantine the initiating document or email and assess whether similar content was delivered to other users.
  - If a script is involved, collect and review the script contents and investigate how it was introduced (downloads, email attachments, shared drives, logon scripts, scheduled tasks).
  - If account compromise is suspected, follow established identity response procedures (credential reset, session review, and access auditing).

- If the activity is confirmed benign:
  - Document the expected parent process, command-line pattern, and destinations.
  - Consider adding a narrowly scoped exception using stable identifiers and constrained conditions (for example, specific `process.command_line` patterns and known destinations) to reduce recurring noise.

