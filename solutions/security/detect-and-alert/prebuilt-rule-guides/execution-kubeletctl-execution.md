---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Kubeletctl Execution Detected via Defend for Containers" prebuilt detection rule.
---

# Potential Kubeletctl Execution Detected via Defend for Containers

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Kubeletctl Execution Detected via Defend for Containers

This detects an interactive execution of kubeletctl within a Linux container, a tool that simplifies direct access to the node’s Kubelet API. It matters because kubeletctl can expose pod and node details and enable actions that support discovery and lateral movement from a compromised container. A common attacker pattern is running `kubeletctl scan` against the Kubelet endpoint, then using `pods` or `exec/attach` to reach other workloads.

### Possible investigation steps

- Determine how an interactive shell was obtained in the container (e.g., kubectl exec, docker exec, or an app RCE) by correlating the timestamp with Kubernetes audit logs and upstream access logs for the initiating user or workload.  
- Review the full kubeletctl invocation to identify the intended operation and target Kubelet endpoint (node IP/hostname and port), then validate whether that endpoint should be reachable from this pod in the cluster design.  
- Correlate container network activity around the alert for connections to node addresses on Kubelet ports (commonly 10250/10255) and look for scanning patterns across multiple nodes indicating discovery or lateral movement attempts.  
- Check for access to Kubernetes credentials within the container (service account token, mounted certificates, kubeconfig, cloud metadata credentials) and verify whether any were used to authenticate to the Kubelet API.  
- Hunt for follow-on actions consistent with lateral movement or impact, such as kubeletctl exec/attach/portForward usage, access to other pod namespaces, or subsequent Kubernetes API activity that creates/patches workloads.

### False positive analysis

- An administrator or developer may have executed kubeletctl interactively inside the container during an incident response or troubleshooting session to enumerate pods/runningpods or validate Kubelet API connectivity, which can resemble discovery activity.  
- A container image or entrypoint script that includes kubeletctl may be invoked manually for routine diagnostics (e.g., running scan/pods/cri or using --server/-s to target a node), producing an interactive exec event without malicious intent.

### Response and remediation

- Isolate the affected pod by scaling it to zero or applying a deny-all egress policy while preserving the container filesystem and process history needed to reconstruct the kubeletctl command, its target node address, and any output artifacts.  
- Block and alert on pod-to-node access to the Kubelet API (typically 10250/10255) at the network layer, and rotate/revoke any Kubernetes service account tokens or kubeconfigs present in the container if kubeletctl attempted authenticated actions like exec/attach/portForward.  
- Remove kubeletctl and related tooling from the image and redeploy from a known-good build, then perform node/pod hygiene by evicting/restarting the workload and checking for persistence indicators such as added binaries, modified entrypoints, or unexpected cron/init scripts.  
- Recover by re-creating the workload in a clean namespace with least-privilege RBAC, validating no unauthorized pods/replicasets were created and that the service account permissions and mounts match the expected deployment spec.  
- Escalate to the incident response team immediately if kubeletctl targeted multiple nodes, invoked exec/attach/portForward/run/scan, or if there is evidence of access to other namespaces or credential material (service account tokens, cloud metadata credentials) from the container.  
- Harden by enforcing Pod Security Standards (no privileged pods, hostNetwork/hostPID/hostPath restrictions), restricting interactive exec into production pods, and limiting node API exposure by disabling unauthenticated Kubelet endpoints and requiring authenticated/authorized access.

