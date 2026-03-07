---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "File Creation and Execution Detected via Defend for Containers" prebuilt detection rule.'
---

# File Creation and Execution Detected via Defend for Containers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating File Creation and Execution Detected via Defend for Containers

This detects an interactive session inside a running Linux container creating a new file and then executing it moments later, a pattern that often signals hands-on intrusion rather than routine automation. Attackers commonly use an `exec` shell into a pod/container to drop a small script or ELF payload (for reverse shell, credential theft, or host discovery) and run it immediately to establish control or stage a breakout attempt.

### Possible investigation steps

- Correlate the alert time with container runtime and Kubernetes audit logs to identify who started the interactive session (user/service account), from where (source IP), and via what mechanism (kubectl exec/attach, docker exec).  
- Acquire the newly created file from the container filesystem, record hash/size/permissions, and analyze its contents to determine whether it is a script, ELF payload, or staged dropper.  
- Reconstruct the execution chain by reviewing the process tree and interactive shell artifacts (TTY, environment, shell history) to understand the operator’s commands before and after running the file.  
- Inspect the container’s network activity immediately following execution (DNS lookups, new outbound connections, unusual ports/destinations) to confirm or rule out command-and-control or payload download behavior.  
- Validate whether the activity indicates privilege escalation or breakout by checking the node and container for access to sensitive host interfaces (e.g., docker.sock, hostPath mounts, /proc probing) and contain the workload if present.

### False positive analysis

- A developer or SRE uses an interactive shell in the container to create or modify a script/binary for debugging (e.g., `cat`/heredoc/vim writing to `/tmp` or the app directory) and then immediately runs it to reproduce an issue or validate a fix.  
- An operator performs interactive break-glass maintenance by manually writing a short helper script (log collection, configuration validation, one-off remediation) inside the container and executing it right after creation to restore service during an incident.

### Response and remediation

- Immediately isolate the affected workload by cordoning and draining the node or applying a deny-all network policy to the pod/namespace, then terminate the interactive session and stop the container to prevent further execution.  
- Preserve evidence by snapshotting the container filesystem and collecting the created file and any adjacent artifacts (shell history, temp directories, downloaded tools), then compute hashes and submit the file for malware analysis.  
- Eradicate by deleting the compromised pod/container and redeploying from a known-good image, rotating any credentials that may have been exposed in the container environment, and blocking the observed outbound destinations if C2 behavior is present.  
- Escalate to incident response immediately if the executed file attempts host interaction (e.g., accesses docker.sock, /proc, hostPath mounts) or if you observe new privileged containers, node-level processes, or lateral movement to other pods/namespaces.  
- Harden by restricting interactive exec/attach to a small admin group with MFA, enforcing Pod Security/Admission policies to disallow privileged/host mounts, and enabling runtime controls to block execution from writable paths like /tmp and /dev/shm.
