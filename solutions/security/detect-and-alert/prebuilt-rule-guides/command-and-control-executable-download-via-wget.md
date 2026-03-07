---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Executable File Download via Wget" prebuilt detection rule.'
---

# Executable File Download via Wget

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Executable File Download via Wget

This rule detects wget pulling down a Mach-O executable and writing it into commonly abused transient or shared directories on macOS, which often signals payload staging during ingress tool transfer. Attackers frequently run wget from a shell or scripted installer to fetch a second-stage binary into /tmp or /Users/Shared, then immediately execute it to establish command and control or deploy additional tooling.

### Possible investigation steps

- Pivot from the detected wget process to identify its parent process, user context, and full command line to determine whether it was launched by an interactive shell, script, or installer package.  
- Review the network connection details from the wget execution (remote IP/domain, URL path, TLS certificate/SNI if available) and assess reputation plus whether it aligns with known internal software distribution.  
- Inspect the downloaded Mach-O at the destination path by collecting its hash, signature/notarization status, and basic static traits (strings, embedded URLs, ad-hoc signing) to quickly judge legitimacy.  
- Check for immediate follow-on activity from the same host such as execution of the new file, creation of persistence (LaunchAgents/Daemons, cron, login items), or additional tool downloads within the next few minutes.  
- Scope for reuse by searching across endpoints for the same downloaded hash, filename, URL, or destination directory pattern to determine blast radius and whether this is a recurring delivery mechanism.

### False positive analysis

- An administrator or developer uses wget in a script to fetch an internal build or test Mach-O binary and stages it in /tmp or /Users/Shared for immediate execution during troubleshooting or CI-style workflows.  
- A legitimate installation or update routine invokes wget to download a helper executable to a transient directory (for unpacking or preflight checks) before moving it into an application bundle, causing a short-lived write to /tmp-like paths.

### Response and remediation

- Isolate the affected macOS host from the network and terminate the active `wget` process to stop additional payload transfers or execution.  
- Quarantine the downloaded Mach-O from `/tmp`, `/private/tmp`, `/var/tmp`, or `/Users/Shared` and preserve a copy plus the originating `wget` command/URL for analysis before removal.  
- Hunt on the host for immediate follow-on execution of the downloaded file and remove any persistence artifacts created around the same time, such as new LaunchAgents/LaunchDaemons, login items, or cron entries pointing to the staged path.  
- Block the observed download URL/domain/IP at egress controls and add allowlisting controls for approved internal distribution sources to reduce future misuse of `wget` for tool transfer.  
- Escalate to incident response if the staged Mach-O is executed, unsigned/ad-hoc signed, establishes outbound connections to unapproved infrastructure, or the same hash/URL is found on multiple endpoints.  
- Harden endpoints by restricting `wget` usage where possible, enforcing Gatekeeper/notarization and least-privilege execution, and adding monitoring/controls for executable writes and executions from world-writable directories.
