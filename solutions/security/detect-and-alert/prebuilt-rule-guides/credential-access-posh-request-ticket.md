---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "PowerShell Kerberos Ticket Request" prebuilt detection rule.
---

# PowerShell Kerberos Ticket Request

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating PowerShell Kerberos Ticket Request

This alert indicates that PowerShell script block content referenced `KerberosRequestorSecurityToken`, a .NET type that can be used to request Kerberos service tickets. In adversary tradecraft, repeated or targeted service ticket requests can support Kerberoasting by obtaining ticket material for offline password cracking of service accounts.

#### Key alert fields to review

- `user.name`, `user.domain`, `user.id`: Account execution context for correlation, prioritization, and scoping.
- `host.name`, `host.id`: Host execution context for correlation, prioritization, and scoping.
- `powershell.file.script_block_text`: Script block content that matched the detection logic.
- `powershell.file.script_block_id`, `powershell.sequence`, `powershell.total`: Script block metadata to pivot to other fragments or reconstruct full script content when split across multiple events.
- `file.path`, `file.directory`, `file.name`: File-origin context when the script block is sourced from an on-disk file.
- `powershell.file.script_block_length`: Script block length (size) context.

#### Possible investigation steps

- Analyze `powershell.file.script_block_text` to determine whether the reference reflects active ticket requesting or incidental text:
  - Identify instantiation patterns (for example, creating a new `KerberosRequestorSecurityToken` object) versus references in comments, strings, or documentation.
  - Identify any service identifiers in the script (for example, SPN-like strings in the form `SERVICE/HOST`) to understand which services are being targeted.
  - Look for signs of bulk activity (loops, arrays/lists of targets, or repeated ticket requests) that would be atypical for troubleshooting and more consistent with Kerberoasting.
  - Look for evidence of ticket material handling or staging (formatting large blobs, encoding/decoding, writing output to disk, or preparing data for transfer) in the same or nearby script blocks.

- Reconstruct complete script content when split across multiple events:
  - If `powershell.total` indicates multiple fragments, pivot on `powershell.file.script_block_id` and order by `powershell.sequence` to rebuild the full script block before drawing conclusions.
  - Note whether the detected fragment is a helper function, an imported module snippet, or part of a larger multi-stage script.

- Use script size and origin to guide triage:
  - Review `powershell.file.script_block_length` to understand whether the script block is a small snippet or a larger embedded tool/module.
  - Review `file.path`, `file.directory`, and `file.name` (when present) to determine whether the script originated from a controlled location. If these fields are absent, treat the activity as potentially interactive or fileless and prioritize reconstructing the full script content.

- Validate execution context and expectedness:
  - Review `user.name`, `user.domain`, and `user.id` to determine whether the account is expected to perform Kerberos troubleshooting or authentication testing from PowerShell.
  - Review `host.name` and `host.id` to determine whether the host is an expected administrative endpoint (for example, a management workstation) or an atypical system for this activity.
  - Check for repeated alerts for the same `user.id` or `host.id` over a short period, which can indicate automation or systematic targeting.

- Assess potential scope and impact:
  - Identify whether the same script content (or the same file name/path, when available) appears across multiple hosts or users, which can indicate a distributed execution campaign.
  - If the script content indicates specific target services, identify the corresponding service accounts in your identity inventory and prioritize high-privilege or broadly scoped services for review.

- Correlate with adjacent telemetry around `@timestamp` (if available in your environment):
  - Review authentication auditing on domain controllers for Kerberos service ticket requests near the alert time and attribute requests to the initiating account and source host to confirm whether ticket requests occurred and whether there was a burst across multiple services.
  - Review endpoint process telemetry for the same host and time window to identify how PowerShell was initiated and whether the parent activity aligns with an expected administrative workflow.
  - Review other PowerShell script block events for the same `user.id` and `host.id` before and after the alert for follow-on behaviors such as discovery, credential access, persistence, or data staging.

- Scope the behavior across the environment:
  - Search for additional occurrences of `KerberosRequestorSecurityToken` in `powershell.file.script_block_text` to identify other potentially affected hosts, users, or time periods.
  - Compare the observed script content and file origin (when available) with known-good scripts to determine whether the behavior is novel or consistent with approved operational activity.

### False positive analysis

- Legitimate Kerberos troubleshooting, authentication validation, or service connectivity testing can request service tickets from PowerShell, especially in environments with custom identity tooling.
- Some administrative automation may request service tickets for a small, fixed set of internal services as part of health checks or integration testing.
- Benign activity is more likely when the script source is known and controlled, the executing account and host are expected for identity administration, and the behavior is limited in scope (few services, short duration, no evidence of ticket material staging).

### Response and remediation

- If the activity is confirmed or strongly suspected malicious:
  - Follow incident response procedures to contain the affected host(s) and prevent additional credential access and lateral movement.
  - Identify the services and accounts potentially targeted based on the script content and Kerberos auditing, then prioritize credential rotation for impacted service accounts and review their privilege and group memberships.
  - Hunt for additional evidence of ticket collection and cracking workflows by reviewing related PowerShell script blocks on the same host/user and by reviewing Kerberos service ticket request patterns over the same time period.
  - Assess whether the initiating user account is compromised and take appropriate actions (credential reset, session invalidation, and access review) based on your organization's response process.

- If the activity is confirmed benign:
  - Document the script owner, purpose, and expected execution context (expected `user.name`, `host.name`, and script location) to speed up future triage.
  - Where possible, move scripts to controlled locations and limit execution to authorized administrative accounts and hosts.
  - Continue monitoring for deviations, such as execution by new accounts, execution from unusual hosts, or expansion to a larger set of targeted services.

