---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "BPF Program or Map Load via bpftool" prebuilt detection rule.
---

# BPF Program or Map Load via bpftool

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating BPF Program or Map Load via bpftool

This rule flags bpftool executions that load, attach, run, or pin eBPF programs and that create or pin maps/links, actions that can change kernel behavior without traditional user-space artifacts. Adversaries can use bpftool to load a malicious eBPF object, attach it to a tracepoint or traffic control hook, and pin the program and maps in bpffs so it persists and hides or filters activity across reboots.

### Possible investigation steps

- Capture full command line, parent process, user context, TTY/session, and current working directory to determine whether execution was interactive administration or automated tooling.  
- Enumerate loaded and pinned eBPF artifacts and their attachment points using `bpftool prog show`, `bpftool map show`, `bpftool link show`, and a filesystem review of `/sys/fs/bpf` to identify unexpected persistence.  
- Identify the eBPF object/source used for the load (path, inode, hash, package origin) and retrieve a copy for analysis, including checking for recent writes or downloads in the same directory tree.  
- Correlate the event time with system logs and other telemetry for follow-on activity such as privilege escalation, module loads, network filtering changes, or suspicious process hiding indicators.  
- Hunt for persistence mechanisms that would reload the same eBPF program after reboot (systemd units/timers, cron, init scripts, container entrypoints) and validate against known legitimate observability/network stacks in the environment.

### False positive analysis

- A system administrator or SRE may run `bpftool prog load/attach/pin` or `bpftool map create/pin` during planned troubleshooting or performance investigation to temporarily instrument kernel events and persist objects under `/sys/fs/bpf` for multi-step validation.  
- A legitimate system service or boot-time automation may invoke `bpftool` to load and pin eBPF programs/maps as part of expected networking, security policy enforcement, or observability initialization, especially after upgrades or configuration changes that trigger reloading.

### Response and remediation

- Immediately isolate the host or container from the network and stop the initiating service/session, then detach any active hooks by removing pinned artifacts under `/sys/fs/bpf` and verifying with `bpftool prog show` and `bpftool link show` that the suspicious program/link is no longer attached.  
- Preserve evidence by collecting the full `bpftool` command line and parent chain, a recursive copy of `/sys/fs/bpf`, and the exact eBPF object file used for the load (path, hash, permissions, timestamps) before deleting or modifying artifacts.  
- Eradicate persistence by removing malicious eBPF pins, deleting or quarantining the associated `.o`/loader binaries, and disabling the boot-time mechanism that reloads them (systemd unit/timer, cron, init scripts, container entrypoint) followed by a controlled reboot to clear any remaining in-kernel state.  
- Recover by restoring the system to a known-good configuration, validating expected networking/observability behavior, and monitoring that no new pinned programs/maps/links reappear under `/sys/fs/bpf` after reboot or service restarts.  
- Escalate to incident response and kernel/rootkit specialists if the program attaches to security-relevant hooks (e.g., tracepoints/kprobes/LSM/tc) or if pinned objects reappear after removal, indicating an active persistence mechanism or compromised privileged runtime.  
- Harden by restricting `bpftool` availability and access to bpffs, enforcing least-privilege for CAP_BPF/CAP_SYS_ADMIN, requiring signed/managed eBPF loaders, and enabling controls that limit eBPF usage to approved components in production images and hosts.
