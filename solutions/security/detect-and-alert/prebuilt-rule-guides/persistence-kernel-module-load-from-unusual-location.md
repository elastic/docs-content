---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kernel Module Load from Unusual Location" prebuilt detection rule.
---

# Kernel Module Load from Unusual Location

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kernel Module Load from Unusual Location

This rule detects attempts to load Linux kernel modules from atypical directories, which can indicate an attacker trying to run code in kernel space for stealth and long-term persistence. Adversaries often drop a malicious `.ko` into writable paths like `/tmp` or `/dev/shm` after initial access, then use `insmod` or `modprobe` to insert it and hide processes, files, or network activity as a rootkit.

### Possible investigation steps

- Capture the full command line and resolve any referenced `.ko` path, then collect the module file for hashing and static analysis to determine provenance and known-malware matches.  
- Confirm whether the module is currently loaded by querying `lsmod`/`/proc/modules`, then map it to its on-disk location with `modinfo -n <module>` (or `/sys/module/<module>/sections/*`) to validate it was loaded from the suspicious directory.  
- Review recent kernel and audit telemetry (`dmesg`, `/var/log/kern.log`, `journalctl -k`, and any audit records) around the event time for insertion messages, signature/taint indicators, and any follow-on errors suggesting tampering.  
- Identify the initiating user/session and execution chain (parent process tree, TTY/SSH source, container context), then determine whether the action aligns with legitimate admin activity or coincides with other compromise signals on the host.  
- Hunt for persistence and repeatability by checking for recurring module-load attempts and inspecting boot-time and scheduled execution paths (systemd units, init scripts, cron, rc.local) that could reload the module after reboot.

### False positive analysis

- A system administrator or automated maintenance workflow may build or test an out-of-tree kernel module and load it with `insmod`/`modprobe` from a staging directory such as `/tmp`, `/root`, or `/mnt` before installing it into standard module paths.  
- A legitimate bootstrapping or recovery operation may load a required driver module from nonstandard media or temporary runtime locations (e.g., `/boot`, `/run`, `/var/run`, or `/mnt`) during troubleshooting, initramfs/early-boot tasks, or mounting encrypted/storage devices.

### Response and remediation

- Isolate the affected Linux host from the network and disable external access (e.g., revoke SSH keys or block inbound SSH) to prevent additional module loads or lateral movement while preserving evidence.  
- If the suspicious module is currently loaded, record `lsmod` and `modinfo` output, then unload it where safe (`modprobe -r <name>`/`rmmod <name>`) and quarantine the corresponding `.ko` from the unusual path (e.g., `/tmp`, `/dev/shm`, `/home`, `/mnt`) for hashing and malware analysis.  
- Remove persistence mechanisms that would reload the module by deleting or disabling any related systemd units, init scripts, cron entries, and boot-time hooks, and validate `/etc/modules-load.d/`, `/lib/modules/$(uname -r)/`, and `depmod` outputs for unauthorized additions.  
- Recover the host by restoring known-good kernel/module packages and rebuilding the initramfs, then reboot and verify no unexpected modules remain in `/proc/modules` and no new load attempts occur from writable directories.  
- Escalate immediately to IR/forensics and consider full host rebuild if the module is unsigned/unknown, the kernel is tainted, module removal fails, or post-reboot evidence indicates stealth behavior consistent with a rootkit.  
- Harden by restricting module loading (enable Secure Boot/module signature enforcement where supported, set `kernel.modules_disabled=1` after boot on fixed-function systems, and limit `CAP_SYS_MODULE` to trusted admins), and enforce file integrity monitoring/permissions to prevent `.ko` creation in world-writable locations.
