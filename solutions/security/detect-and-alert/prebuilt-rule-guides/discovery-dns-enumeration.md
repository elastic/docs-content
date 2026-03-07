---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "DNS Enumeration Detected via Defend for Containers" prebuilt detection rule.
---

# DNS Enumeration Detected via Defend for Containers

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating DNS Enumeration Detected via Defend for Containers

This rule flags interactive use of DNS utilities (nslookup, dig, host, or getent hosts) inside a Linux container that query internal Kubernetes names such as kubernetes.default or *.svc.cluster.local, signaling in-cluster service discovery. After compromising a pod, an attacker opens an interactive shell and runs nslookup kubernetes.default or dig *.svc.cluster.local to enumerate services and namespaces, map reachable endpoints, and stage lateral movement toward the API server, internal dashboards, or other pods.

### Possible investigation steps

- Correlate with Kubernetes audit logs to see if a kubectl exec/attach or ephemeral container was launched into this pod at the same time and identify the requesting user, source IP, and service account identity.
- Pull pod metadata (namespace, owner workload, node, image digest, service account) and verify whether this is a sanctioned troubleshooting/debug context by checking image baseline and change tickets.
- Examine command history and process lineage within the container around the alert to spot follow‑on actions such as reading /var/run/secrets/kubernetes.io/serviceaccount, querying the API server, installing tools, or scanning internal ranges.
- Review DNS and network telemetry from the pod (CoreDNS logs, CNI flow logs) to map the queried hostnames and any subsequent connections to internal services or the API server.
- If unauthorized activity is suspected, isolate the pod via network policy or eviction, rotate the pod’s service account token and related secrets, and redeploy from a trusted image while investigating node and registry access paths.

### False positive analysis

- An authorized operator attaches an interactive shell to a pod for in-cluster troubleshooting and runs nslookup/dig/host or getent hosts against kubernetes.default or *.svc.cluster.local, matching the rule but expected.
- A pod or initContainer configured with tty: true or stdin enabled executes startup/readiness logic that calls getent hosts or nslookup on internal service FQDNs (*.svc.cluster.local), which is benign but appears as interactive enumeration.

### Response and remediation

- Immediately isolate the affected pod by applying a deny‑egress NetworkPolicy to the CoreDNS service and cluster service CIDRs, terminate the interactive shell that ran nslookup/dig/host or getent hosts, and temporarily block kubectl exec/attach to the workload.
- Evict the pod and redeploy from a trusted image digest, removing any ephemeral containers added for debugging and uninstalling ad‑hoc packages (e.g., dnsutils, busybox) that were introduced into the container.
- Rotate credentials by deleting and reissuing the workload’s service account token and any mounted secrets or registry credentials, then verify the new pod does not perform interactive lookups of kubernetes.default or *.svc.cluster.local.
- Escalate to incident response if enumeration originates from a production namespace, a privileged service account, or is followed by reading /var/run/secrets/kubernetes.io/serviceaccount or curl/wget to https://kubernetes.default, or if similar activity is observed across multiple pods.
- Harden going forward by restricting exec/attach via RBAC, enforcing Admission Controls/Pod Security to disallow tty/stdin and unauthorized ephemeral containers, limiting egress to CoreDNS and internal services with NetworkPolicies, and using distroless/stripped images that omit nslookup/dig/host.

