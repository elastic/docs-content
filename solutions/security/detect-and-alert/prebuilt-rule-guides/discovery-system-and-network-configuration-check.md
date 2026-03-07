---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "System and Network Configuration Check" prebuilt detection rule.'
---

# System and Network Configuration Check

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating System and Network Configuration Check

This rule flags suspicious processes reading macOS SystemConfiguration preferences, which can reveal network interfaces, DNS settings, and other environment details used to plan lateral movement or data exfiltration. Attackers commonly run scripting runtimes (e.g., Python, AppleScript, Node) or binaries staged in temporary/shared directories to open the preferences plist during early discovery. Catching this access helps identify stealthy reconnaissance before overt network activity begins.

### Possible investigation steps

- Identify the parent process and full execution chain for the accessing process, including any script path/arguments, to determine whether it was launched by an interactive user, management tooling, or a suspicious launcher.  
- Review the accessing binary’s provenance by checking code signature/notarization status, file hash reputation, and whether it was recently created or executed from temporary/shared directories indicating staging.  
- Correlate nearby discovery activity on the host (e.g., reads of other system/network plists, execution of `scutil`, `ifconfig`, `networksetup`, or `defaults read`) to assess whether this is part of a broader reconnaissance sequence.  
- Examine concurrent network activity from the same process (outbound connections, DNS lookups, proxy changes) to identify follow-on behavior consistent with environment mapping or command-and-control.  
- Validate the behavior against legitimate software on the host (IT management, VPN/endpoint tools, developer workflows) by matching timestamps to user logins, scheduled jobs, and recent installs/updates.

### False positive analysis

- A legitimate IT/admin or troubleshooting script run interactively (e.g., a Python/AppleScript wrapper) may read `/Library/Preferences/SystemConfiguration/preferences.plist` to collect network settings during support, onboarding, or diagnostics.  
- A developer or automation workflow may execute a temporary or shared-directory runtime (e.g., `node`/`python` unpacked to `/tmp` or `/Users/Shared`) that reads the plist to detect interfaces, DNS, or proxy configuration for environment-aware builds or tests.

### Response and remediation

- Isolate the affected Mac from the network and terminate the offending process tree, then quarantine the on-disk script/binary (especially if staged in /tmp, /private/tmp, /var/tmp, or /Users/Shared) to stop further discovery or follow-on execution.  
- Collect and preserve artifacts before cleanup, including the suspicious executable/script, its launch mechanism (LaunchAgents/LaunchDaemons, cron, login items), recent shell history, and a copy of /Library/Preferences/SystemConfiguration/preferences.plist metadata for later scoping and forensics.  
- Eradicate persistence by removing unauthorized launch entries and deleting the staged payloads, then re-scan the host with EDR/AV and verify no additional suspicious interpreters or unsigned tools remain in temporary/shared directories.  
- Recover by rotating credentials used on the host, reviewing and resetting network settings (DNS, proxy, VPN) if changed, and returning the system to service only after repeated checks show no re-creation of the removed artifacts across a full reboot cycle.  
- Escalate to incident response immediately if the same process also makes outbound connections, modifies SystemConfiguration plists, or appears on multiple hosts, and initiate enterprise-wide hunting for the file hash and the associated launcher.  
- Harden by restricting execution from temporary/shared directories, enforcing signed/notarized code where possible, auditing who can read sensitive configuration files, and adding allowlists for known management tools that legitimately access the preferences plist.
