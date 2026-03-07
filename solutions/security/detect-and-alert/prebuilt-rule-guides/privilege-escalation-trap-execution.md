---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Trap Signals Execution" prebuilt detection rule.
---

# Trap Signals Execution

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Trap Signals Execution

This rule flags use of the shell built-in trap to bind commands to POSIX signals, enabling automatic execution when interrupts like SIGINT, SIGHUP, or SIGTERM occur. Attackers commonly embed traps in bash, zsh, or service scripts so pressing Ctrl+C (SIGINT) or a daemon reload (SIGHUP) silently runs a payload—adding a user to sudoers, planting a setuid helper, or launching a reverse shell—achieving persistence or escalation without a direct command invocation.

### Possible investigation steps

- Pull the full trap command and its arguments plus the parent script path, then read the script to see which signals map to which payloads and whether they perform user, permission, or network actions.
- Determine execution context by user and privilege, TTY/session versus systemd or cron, and whether the shell was invoked with sudo or as root to gauge impact if the trap triggers.
- Correlate telemetry for signal delivery (kill, hangup, termination) to the same process and for immediate follow-on activity such as child process spawns, edits to /etc files, setuid or chmod events, and outbound connections.
- Search the host for other trap definitions in login and init paths (.bashrc, .zshrc, /etc/profile, /etc/*rc, systemd unit scripts, and cron wrappers) to identify persistence or broader tampering.
- Verify legitimacy by comparing the script to package or repository sources and change records, and preserve artifacts (path, hash, mtime, owner) along with shell history and environment for deeper analysis.

### False positive analysis

- Operations or maintenance scripts legitimately declare trap handlers for SIGTERM or SIGHUP to perform cleanup during routine shutdown or reload, producing trap commands with signal arguments that match this detection.
- Interactive shell customization may set a trap on SIGINT (Ctrl+C) to restore terminal settings or print a message on interruption, resulting in benign trap invocations with SIG* arguments.

### Response and remediation

- Isolate the host or TTY session where a trap binds SIGINT/SIGHUP/SIGTERM to commands that write to /etc or open a socket, kill the offending shell and its parent process, and stop/disable any systemd unit or cron wrapper invoking the implicated script path.
- Edit the identified script or rc file (.bashrc, .zshrc, /etc/profile, systemd unit script) to remove or unset the trap handlers, and delete or quarantine any referenced payload such as a reverse-shell binary, sudoers drop-in, or setuid helper.
- Restore altered files from a known-good baseline (e.g., /etc/sudoers, unit .service files, shell RCs), revalidate file ownership and permissions, restart impacted services cleanly, and rotate credentials for users touched by the payload.
- Sweep the host and peers for additional trap definitions by grepping for "trap SIG" in login/init paths and service scripts, and record script path, hash, mtime, and owner to confirm scope and support cleanup.
- Escalate to incident response if the trap executes as root, modifies /etc/sudoers or PAM files, creates setuid files under /usr/bin or /usr/local/bin, or starts a reverse shell to an external IP/port.
- Harden by restricting write access to /etc/*rc and service scripts, enforcing deployment via signed packages, adding audit rules for changes to /etc/sudoers and /etc/profile.d, blocking shells from egress to untrusted networks, and alerting on traps bound to EXIT/DEBUG or signals that invoke privileged actions.

