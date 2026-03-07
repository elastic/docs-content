---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kubelet Pod Discovery Detected via Defend for Containers" prebuilt detection rule.'
---

# Kubelet Pod Discovery Detected via Defend for Containers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubelet Pod Discovery Detected via Defend for Containers

This rule detects interactive use of common Linux utilities (ls, find, du, locate, nice) repeatedly targeting the Kubelet pods directory, including direct access to `/var/lib/kubelet/pods/*`. This matters because enumerating that path reveals pod IDs, volumes, and runtime artifacts that can accelerate container and cluster discovery. A typical pattern is an attacker in a compromised container running `ls /var/lib/kubelet/pods/` followed by `find /var/lib/kubelet/pods -maxdepth 2` to map workloads and hunt for mounted secrets.

### Possible investigation steps

- Identify the originating workload (pod/namespace/node) and how the interactive session was obtained (e.g., kubectl exec, SSH to node, or container runtime attach) to determine whether access was expected.  
- Review the container’s security context and mounts to confirm whether `/var/lib/kubelet` was exposed via hostPath/privileged settings and assess whether this indicates a node breakout risk.  
- Correlate the discovery activity with nearby events for follow-on actions such as reading service account tokens, kubeconfig files, or secrets/volumes under pod directories that would indicate credential harvesting.  
- Validate the actor by mapping the involved user/service account to recent Kubernetes API audit activity and RBAC permissions to determine whether the behavior aligns with normal administration.  
- Check for persistence or lateral movement attempts from the same container or node (new processes, outbound connections, package/tool downloads, or cron/systemd changes) to scope impact beyond discovery.

### False positive analysis

- An interactive troubleshooting session by a cluster administrator inside a privileged/host-mounted container uses `ls`, `find`, or `du` against `/var/lib/kubelet/pods/*` multiple times to confirm pod volume mounts, disk usage, or pod UID-to-workload mapping during an incident or maintenance window.  
- An engineer running an interactive shell on the node or in a hostPID/hostPath-enabled container repeatedly inspects `/var/lib/kubelet/pods/*` with built-in utilities to validate kubelet behavior (e.g., orphaned pod directories, cleanup after pod churn, or verifying that expected pods are present) as part of routine operational checks.

### Response and remediation

- Contain by terminating the interactive session and isolating the originating pod (scale to zero or delete) and, if the container had hostPath access to `/var/lib/kubelet` or was privileged/hostPID, cordon and drain the node to stop further inspection of `/var/lib/kubelet/pods/*`.  
- Scope and eradicate by reviewing recent commands and file reads under `/var/lib/kubelet/pods/` for access to mounted secrets, service account tokens, kubeconfig files, or pod volume contents, and remove any dropped tools/scripts or unauthorized cron/systemd changes on the affected node.  
- Recover by rotating potentially exposed Kubernetes credentials (service account tokens, kubeconfigs, cloud/IAM keys) used by the affected workload and redeploying the application from a known-good image after validating no unexpected containers, DaemonSets, or mounts remain.  
- Escalate to incident response immediately if you confirm reads of token/secret material within pod directories, discovery occurs from a privileged or host-mounted container, or you observe follow-on actions such as outbound connections, new binaries, or attempts to exec into additional pods/namespaces.  
- Harden by eliminating unnecessary hostPath mounts to `/var/lib/kubelet` (and other node paths), enforcing non-root and read-only root filesystems, disabling interactive shells in production where feasible, and applying admission controls to block privileged/hostPID containers and restrict debug tooling to approved break-glass workflows.
