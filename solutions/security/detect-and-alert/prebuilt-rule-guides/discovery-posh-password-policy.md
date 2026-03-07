---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "PowerShell Script with Password Policy Discovery Capabilities" prebuilt detection rule.
---

# PowerShell Script with Password Policy Discovery Capabilities

## Triage and analysis

> **Disclaimer**:
> This guide was created by humans with the assistance of generative AI. While its contents have been manually curated to include the most valuable information, always validate assumptions and adjust procedures to match your internal runbooks and incident triage and response policies.

### Investigating PowerShell Script with Password Policy Discovery Capabilities

This alert identifies PowerShell script block content consistent with querying Active Directory password policy settings, including default domain policy requirements, fine-grained password policies, or related directory attributes. Adversaries may use these details to tune password guessing attempts and prioritize targets; administrators may also collect this information for auditing and troubleshooting.

#### Key alert fields to review

- `user.name`, `user.domain`, `user.id`: Account execution context for correlation, prioritization, and scoping.
- `host.name`, `host.id`: Host execution context for correlation, prioritization, and scoping.
- `powershell.file.script_block_text`: Script block content that matched the detection logic.
- `powershell.file.script_block_id`, `powershell.sequence`, `powershell.total`: Script block metadata to pivot to other fragments or reconstruct full script content when split across multiple events.
- `file.path`, `file.directory`, `file.name`: File-origin context when the script block is sourced from an on-disk file.
- `powershell.file.script_block_length`: Script block length (size) context.

#### Possible investigation steps
- Review `powershell.file.script_block_text` and identify the discovery method:
  - AD password policy cmdlets/functions such as `Get-ADDefaultDomainPasswordPolicy`, `Get-ADFineGrainedPasswordPolicy`, `Get-ADUserResultantPasswordPolicy`, `Get-DomainPolicy`, or `Get-PassPol`.
  - Directory searcher patterns such as `defaultNamingContext`, `ActiveDirectory.DirectoryContext`, or `ActiveDirectory.DirectorySearcher`, and referenced properties/attributes like `.MinLengthPassword`, `.MinPasswordAge`, `.MaxPasswordAge`, `minPwdLength`, `minPwdAge`, `maxPwdAge`, or `msDS-PasswordSettings`.
  - Helper function use that may attempt to access Group Policy Preference password data (for example, `Get-GPPPassword`).
- Determine scope and intent from the script content:
  - Domain-wide enumeration vs querying a specific user/resultant policy.
  - Enumeration of fine-grained policy objects (`msDS-PasswordSettings`), which can indicate targeted reconnaissance for weaker settings.
  - Evidence of output collection (formatting, exporting, or writing results) that may support later use.
- Validate the execution context using `host.name`, `host.id`, `user.name`, `user.domain`, and `user.id`:
  - Confirm the host is an expected location for administrative or audit activity (for example, an admin workstation or management server).
  - Assess whether the account context aligns with expected job function and normal host access patterns.
- Determine script origin and how it was introduced when `file.path`, `file.directory`, or `file.name` are present:
  - Validate that the script path and name align with approved tooling and standard locations for that host.
  - Treat execution from user-writable or temporary locations, or from unfamiliar script names, as higher risk and scope for additional suspicious activity.
- Reconstruct the full script content when it is split across multiple events:
  - Pivot on `powershell.file.script_block_id` and order by `powershell.sequence` to rebuild the full script (use `powershell.total` to confirm all fragments are present).
  - Preserve the reconstructed content for case notes and scoping.
- Correlate with other activity from the same host and account near `@timestamp` (if available in your telemetry):
  - Review additional PowerShell script block logs for related discovery, credential access attempts, or follow-on execution.
  - Review process activity to determine how PowerShell was launched (parent process, service/automation context, or interactive use) and whether the launch source is expected for the user/host.
  - Review network activity consistent with directory queries or access to domain infrastructure that may indicate broader reconnaissance.
  - Review file activity for evidence of staged scripts/modules or stored output containing policy details.
  - Review authentication activity for spikes in failed logons, account lockouts, or access to multiple hosts following the discovery.
- Scope and prevalence:
  - Look for similar `powershell.file.script_block_text` content executed by the same `user.id` on other hosts to determine whether this is isolated or part of a wider discovery phase.
  - Look for similar content on the same `host.id` from other users to identify shared tooling, automation, or a compromised host used to launch reconnaissance.

### False positive analysis
- Authorized identity and directory administration activities (for example, validating password policy requirements during audits, troubleshooting, or policy change reviews).
- Scheduled reporting or compliance workflows that periodically inventory default and fine-grained password policy settings.
- Support investigations that query resultant password policy for a specific user as part of account lifecycle management or lockout investigations.

### Response and remediation
- If the activity is unexpected or cannot be tied to an approved administrative task:
  - Isolate the affected host to prevent further reconnaissance.
  - Restrict or disable the involved account (`user.id`) and reset credentials according to incident response procedures.
  - Preserve evidence, including the reconstructed `powershell.file.script_block_text`, associated `powershell.file.script_block_id` fragments, and any referenced scripts (`file.path`, `file.name`).
  - Hunt for follow-on activity associated with password policy discovery, such as password guessing attempts, credential collection, and additional directory enumeration, using the same `user.id`, `host.id`, and timeframe.
  - If the script content suggests access to Group Policy Preference password data, treat this as potential credential exposure and rotate any identified credentials and remediate insecure configurations.
- If the activity is confirmed benign:
  - Document the approved use case (expected accounts, hosts, and script locations) to speed future triage.
  - Apply least-privilege controls to limit where and by whom directory policy discovery can be performed while maintaining audit visibility.

