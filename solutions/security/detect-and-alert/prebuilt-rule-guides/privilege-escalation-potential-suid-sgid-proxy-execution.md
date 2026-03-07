---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Privilege Escalation via SUID/SGID Proxy Execution" prebuilt detection rule.
---

# Potential Privilege Escalation via SUID/SGID Proxy Execution

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Privilege Escalation via SUID/SGID Proxy Execution

This rule surfaces executions of well-known SUID/SGID helpers on Linux that run with root privileges while the launching user remains non‑root, signaling an attempt to proxy elevated rights. It matters because a non‑privileged process invoking pkexec can spawn /bin/sh as root via environment manipulation, turning a low-privilege foothold into full system control.

### Possible investigation steps

- Determine if the invocation is interactive and expected (e.g., admin using su/sudo) by correlating with a TTY/SSH session, recent successful authentication logs, and sudo/polkit policy outcomes in journald.
- For pkexec events, inspect the environment for exploit indicators (e.g., unset argv or suspicious GCONV_PATH, PATH, LD_PRELOAD, LC_* values) and look for attacker-created files in /tmp or the user's home that match gconv or loader artifacts.
- Review the child/descendant process tree of the SUID/SGID helper to see if it spawned a root shell or arbitrary interpreter, and pivot to concurrent network connections or file writes by those children.
- Validate whether the executable’s SUID/SGID file on disk has been tampered with by checking its hash, permissions, ownership, and recent mtime against package manager metadata and known-good baselines.
- If the binary is mount/umount/fusermount or newuidmap/newgidmap, correlate with container or FUSE activity to confirm a legitimate workflow and inspect mounts or namespace changes for risky options (e.g., suid, exec) or unusual target directories.

### False positive analysis

- An authorized pkexec or polkit-agent-helper invocation by a user to perform a permitted administrative task may run as root while the real user is non‑root, often with a single‑argument parent, and should align with an interactive prompt and expected policy.
- Normal unprivileged workflows using fusermount3 or newuidmap/newgidmap legitimately leverage SUID/SGID helpers, typically launched by a simple shell with one argument, and should correlate with expected mount or user‑namespace activity.

### Response and remediation

- Immediately isolate the host, kill the offending SUID/SGID child processes (e.g., pkexec spawning /bin/sh), and temporarily remove the setuid/setgid bit from the abused binary (chmod u-s /usr/bin/pkexec or chmod g-s /usr/bin/newgrp) to halt further elevation.
- Reinstall and verify integrity of abused packages and SUID helpers (e.g., polkit to replace /usr/bin/pkexec, dbus-daemon-launch-helper, fusermount3) and delete attacker artifacts such as gconv modules or LD_PRELOAD payloads from /tmp, /var/tmp, and user homes.
- Undo attacker changes by restoring /etc/sudoers, /etc/passwd and /etc/shadow, and polkit rules under /usr/share/polkit-1 or /etc/polkit-1, unmount suspicious FUSE or bind mounts created by fusermount3/mount, and rotate credentials and keys.
- Escalate to incident command if you observe a SUID helper launching an interactive root shell (/bin/sh -p or bash -p), root-owned droppers in /tmp or /usr/local/bin, or similar events on more than one host or account.
- Permanently reduce the SUID/SGID attack surface by auditing and removing setuid bits from rarely used binaries (e.g., chfn, chsh, newgrp, ssh-keysign), restricting pkexec via polkit rules to specific callers, and mounting /tmp, /var/tmp, and home directories with nosuid,nodev,noexec.
- Strengthen monitoring and policy by enabling AppArmor/SELinux confinement for pkexec and mount helpers, adding auditd rules for exec of setuid binaries and writes to /tmp by root, and enforcing least-privilege sudoers by removing broad NOPASSWD entries and requiring MFA for privileged tasks.

