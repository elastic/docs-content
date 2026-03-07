---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "PowerShell Mailbox Collection Script" prebuilt detection rule.'
---

# PowerShell Mailbox Collection Script

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating PowerShell Mailbox Collection Script

This alert indicates PowerShell script block content consistent with programmatic mailbox access using Outlook Interop/MAPI or Exchange Web Services (EWS) managed APIs. This can support legitimate administration and support workflows, but it can also be used to collect messages and attachments for discovery or theft. Prioritize determining (1) who ran the script and where, (2) which mailbox(es) and folders were accessed, and (3) whether any content was staged or transferred.

#### Key alert fields to review

- `user.name`, `user.domain`, `user.id`: Account execution context for correlation, prioritization, and scoping.
- `host.name`, `host.id`: Host execution context for correlation, prioritization, and scoping.
- `powershell.file.script_block_text`: Script block content that matched the detection logic.
- `powershell.file.script_block_id`, `powershell.sequence`, `powershell.total`: Script block metadata to pivot to other fragments or reconstruct full script content when split across multiple events.
- `file.path`, `file.directory`, `file.name`: File-origin context when the script block is sourced from an on-disk file.
- `powershell.file.script_block_length`: Script block length (size) context.

#### Possible investigation steps

- Confirm the execution context:
  - Review `user.name`, `user.domain`, and `user.id` to identify the executing account and whether it commonly performs mailbox-related automation.
  - Review `host.name` and `host.id` to identify the endpoint and whether it is expected to run mailbox access scripts.
  - Use the alert time as an anchor to check for other suspicious activity from the same user and host in the surrounding timeframe.

- Analyze `powershell.file.script_block_text` for technique, targeting, and scope:
  - Outlook Interop/MAPI usage commonly includes `Microsoft.Office.Interop.Outlook`, `Interop.Outlook.olDefaultFolders`, `Outlook.Application`, `GetNamespace`/`MAPI`, `Session`, `GetDefaultFolder`, `GetSharedDefaultFolder`, and default folder references such as `olFolderInBox`.
  - EWS usage commonly includes `Microsoft.Exchange.WebServices.Data.ExchangeService`, `Microsoft.Exchange.WebServices.Data.Folder`, `Microsoft.Exchange.WebServices.Data.FileAttachment`, and mailbox enumeration or retrieval methods such as `FindItems`, `Bind`, `WellKnownFolderName`, `FolderId`, `ItemView`, `PropertySet`, `SearchFilter`, and `Attachments`.
  - Identify mailbox identifiers (email addresses, aliases), folder targets (default folders, explicit folder names), and any shared mailbox references.
  - Determine collection breadth by noting loops over folders/items, pagination settings (such as item views), and filtering criteria (date/keyword filters).
  - Identify how items or attachments are handled (enumeration only vs retrieval and save/export) and any referenced storage locations.

- Reconstruct the full script:
  - Pivot on `powershell.file.script_block_id` to collect all fragments related to the same script block.
  - Use `powershell.sequence` and `powershell.total` to order fragments and confirm completeness; missing fragments can change intent and scope.
  - Use `powershell.file.script_block_length` to understand whether the alert contains a short snippet or part of a larger tool.

- Determine script provenance and reuse:
  - If present, review `file.path` and `file.name` to identify the on-disk script/module source and whether the location aligns with expected administrative tooling.
  - If `file.path` is absent, treat the execution as potentially interactive or dynamically loaded; rely on the reconstructed script content to determine intent and scope.
  - Search for the same `file.name`/`file.path` and distinctive strings from `powershell.file.script_block_text` across other hosts and users to identify reuse or deployment.

- Correlate with adjacent telemetry (if available) to identify launch method and downstream activity:
  - Process execution: identify the PowerShell host process and any parent process/launcher to determine whether execution was interactive, automated, or initiated by another application.
  - Network activity: review outbound connections around the alert time for access to Exchange/EWS endpoints and for unexpected external destinations that could indicate transfer of collected data.
  - File activity: review for new or modified files consistent with staging mail content (exports, archives, or attachment dumps), especially in locations referenced by the script.
  - Authentication activity: review for unusual sign-ins or repeated authentications by the executing account that align with mailbox enumeration or access to multiple mailboxes.

- Assess impact and prioritize response:
  - Treat as higher priority when the script references shared mailboxes, multiple mailbox identifiers, broad folder enumeration, or attachment retrieval.
  - Coordinate with messaging administrators to validate whether the access scope is authorized and to help identify potentially affected mailboxes and data types.

### False positive analysis

- Approved administration, reporting, archiving, or migration workflows that programmatically access mailbox data using Outlook Interop/MAPI or EWS.
- Support or troubleshooting activity where staff retrieve specific messages or attachments under an approved request.
- Development or testing of Outlook automation or EWS integrations on non-production hosts.

### Response and remediation

- If unauthorized or suspicious, contain the affected host to prevent continued mailbox access and reduce the risk of data transfer.
- Restrict the executing account (disable or reset credentials based on severity) and review mailbox permissions and delegation associated with the account.
- Preserve evidence for investigation and response:
  - Retain the reconstructed script content and all associated script block events for `powershell.file.script_block_id`.
  - If `file.path` is present, preserve the referenced script/module for forensic review and determine how it was introduced.
- Identify and remediate persistence or automation mechanisms that could re-run the script and expand collection scope.
- Assess and document impact using the reconstructed script content:
  - Determine which mailbox(es), folders, and item types (messages and attachments) were targeted.
  - Identify any local staging locations or transfer destinations referenced by the script.
- Coordinate with messaging administrators and relevant stakeholders to support mailbox-level investigation and response actions if sensitive data may have been accessed.
- Increase monitoring for recurrence by tracking similar script block content, repeated executions by the same user, and reuse of the same script file paths across hosts.
