---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Discovery Command Output Written to Suspicious File" prebuilt detection rule.'
---

# Discovery Command Output Written to Suspicious File

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Discovery Command Output Written to Suspicious File

This rule flags a macOS discovery utility launched from an interactive shell and, within seconds, the same process writing to an unusual or hidden file location, indicating staged reconnaissance for later theft. Adversaries commonly run commands like `whoami`, `ifconfig`, `dscl`, or `system_profiler` and redirect output into `/tmp`, `/Users/Shared`, or a dotfile path to bundle host details before exfiltrating the collected text.

### Possible investigation steps

- Review the created/modified file’s contents, size, and timestamps to confirm it contains discovery output and whether it is being appended across multiple executions.  
- Pivot from the initiating process to identify subsequent child processes or shell commands that compress, encrypt, move, or delete the file, indicating staging and cleanup.  
- Examine concurrent network activity from the same process tree for outbound connections, file uploads, or suspicious DNS/HTTP requests immediately after the write event.  
- Validate the interactive session context by correlating to the logged-in user, terminal/TTY (if available), remote access artifacts (SSH/VPN/remote management), and recent authentication events for that account.  
- Hunt on the host for related staging patterns such as additional hidden files in common drop locations, recent archive creation, or persistence changes (LaunchAgents/LaunchDaemons/crontab) around the alert time.

### False positive analysis

- An administrator or troubleshooting script run from bash/zsh may execute built-in discovery commands (e.g., `system_profiler`, `ifconfig`, `dscl`) and redirect the output into `/tmp`, `/private/tmp`, or `/Users/Shared` as a temporary log or support bundle artifact.  
- A login/profile shell customization (e.g., `.zshrc`/`.bash_profile`) or local diagnostic routine may run `whoami`/`arch`/`csrutil` and append results into a hidden dotfile path (e.g., `/*/.*`) for auditing or environment validation, creating a short command-then-write pattern.

### Response and remediation

- Isolate the macOS host from the network and suspend or terminate the implicated shell/process tree that executed the discovery command and immediately wrote into locations like `/tmp`, `/Users/Shared`, or hidden dotfiles to prevent further staging or exfiltration.  
- Quarantine the written file(s) and any adjacent artifacts (archives, encrypted blobs, renamed copies) from the same directories, preserve them for analysis, and remove the staged data once collection is complete.  
- Identify and eradicate the launch point by reviewing the invoking shell history and user startup scripts (e.g., `.zshrc`, `.bash_profile`) for redirection or scripted discovery, and delete any associated persistence (LaunchAgents/LaunchDaemons, cron entries) tied to the same user or file path.  
- Rotate credentials and invalidate active sessions for the logged-in user that ran the command, and audit recent remote access methods (SSH, remote management, VPN) used on the host to ensure the account was not compromised.  
- Restore the host to a known-good state by reinstalling or reimaging if tampering is suspected, then monitor for re-creation of the same suspicious file paths and repeat discovery-to-file-write behavior from any interactive shell.  
- Escalate to IR leadership immediately if the staged file contains host/user inventory data and there is evidence of outbound transfer attempts (new external connections, upload utilities like `curl`/`scp`, or rapid archive creation) following the write event.
