---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kubelet Certificate File Access Detected via Defend for Containers" prebuilt detection rule.'
---

# Kubelet Certificate File Access Detected via Defend for Containers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubelet Certificate File Access Detected via Defend for Containers

This detection flags an interactive process inside a Linux container opening files under `/var/lib/kubelet/pki/`, which includes the kubelet client certificate and key used to authenticate to the Kubernetes API. Attackers who obtain these credentials can impersonate the node, enumerate cluster resources, and pivot to secrets or workloads. A common pattern is an operator exec’ing into a compromised pod, locating the kubelet cert/key pair, copying it out, then using it to query the API server from outside the container.

### Possible investigation steps

- Identify the pod/namespace/node and owning controller for the container, then confirm whether it should ever have access to host kubelet PKI (e.g., privileged DaemonSet, hostPath mount, node-agent tooling) or if this is an unexpected breakout indicator.
- Review the interactive session context (exec/attach/ssh), including who initiated it and the command history/TTY telemetry around the alert time, to determine whether this was routine debugging or suspicious enumeration.
- Inspect the container filesystem and recent file operations for evidence of credential harvesting (reads of kubelet client cert/key pairs, copies to temporary paths, archive creation, or outbound transfer tooling) and preserve artifacts for forensics.
- Correlate immediately after the access event for Kubernetes API activity using node credentials (unusual discovery, secret access, or cluster-wide queries) originating from the same workload identity, node, or egress address.
- Validate whether kubelet credentials were reused by reviewing API server audit logs for unexpected node identity actions, and rotate kubelet client certs/keys and isolate the workload if misuse is suspected.

### False positive analysis

- A cluster operator or SRE may exec into a privileged pod (e.g., a DaemonSet with hostPath access to `/var/lib/kubelet`) for node troubleshooting and use interactive shell commands to inspect or validate kubelet PKI files during incident response or routine maintenance.
- A legitimate containerized node-management or diagnostic workflow that runs interactively (e.g., invoked manually for verification) may open files under `/var/lib/kubelet/pki/` as part of validating kubelet certificate presence/permissions after upgrades, certificate rotation, or node reconfiguration.

### Response and remediation

- Immediately isolate the affected workload by scaling the pod/controller to zero or cordoning and draining the node if a privileged pod has host access to `/var/lib/kubelet/pki/`, and preserve the container filesystem and process list for forensics before teardown.  
- Remove the execution path that enabled access by deleting or patching the pod/DaemonSet to drop `privileged`, `hostPID/hostNetwork`, and any `hostPath` mounts that expose `/var/lib/kubelet` and redeploy only from a known-good image and manifest.  
- Rotate and reissue kubelet client certificates/keys on the impacted node(s) (or replace the node from autoscaling/immutable infrastructure) and verify the old credentials can no longer authenticate to the Kubernetes API server.  
- Review Kubernetes API server audit logs for activity using the node identity around the access time (cluster-wide discovery, secret reads, token reviews, exec into other pods) and revoke/rotate any exposed service account tokens or secrets accessed during the window.  
- Escalate to the Kubernetes platform/on-call security team immediately if the files include a kubelet client key, if the pod was privileged or had host mounts, or if API audit logs show node credential use from unexpected sources or unusual resource enumeration.  
- Harden the cluster by enforcing policies that block hostPath access to `/var/lib/kubelet` and privileged pods (Pod Security Admission/Gatekeeper/Kyverno), limiting interactive exec/attach via RBAC, and monitoring for subsequent access attempts to kubelet PKI paths and related credential exfiltration tooling.
