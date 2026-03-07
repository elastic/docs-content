---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Direct Interactive Kubernetes API Request Detected via Defend for Containers" prebuilt detection rule.
---

# Direct Interactive Kubernetes API Request Detected via Defend for Containers

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Direct Interactive Kubernetes API Request Detected via Defend for Containers

The rule flags interactive use of curl, wget, openssl, busybox ssl_client, socat/ncat, or kubectl from inside a container to call the Kubernetes API with a bearer token, often with custom CA or insecure TLS options. An operator enumerates cluster resources and tests access with in-pod credentials, enabling lateral movement or privilege escalation; after landing in a pod, they read the service account token and query the API to list namespaces, pods, or secrets, or issue kubectl get/patch to probe or modify workloads.

### Possible investigation steps

- Map the container ID to its pod, namespace, node, image, and owning controller, and confirm whether this workload is expected to make direct Kubernetes API calls or allow interactive access.
- Determine how the interactive session was initiated and by whom by correlating with Kubernetes events and audit logs for exec/attach/ephemeral-container activity and runtime logs for TTY sessions, including the initiating principal and source IP.
- Correlate with API server audit logs to retrieve the exact requests (verbs, resources, namespaces), the authenticated subject (service account or user), and response codes to identify any successful access to sensitive resources like Secrets or workload-modifying actions.
- Inspect the pod for credential use and operator traces by checking recent process activity, shell history, environment variables, and access to service account token or kubeconfig files at expected mount paths.
- Assess scope and potential persistence by listing recent cluster objects created or modified by the same identity across namespaces (Pods, CronJobs, RoleBindings, Secrets) within the timeframe around the alert.

### False positive analysis

- An administrator used kubectl interactively within a maintenance container to run get/list/patch commands during routine operations such as inspecting pods or updating labels, which matches expected administrative behavior.
- A developer ran openssl s_client, socat with SSL, or ncat --ssl interactively from within the container to troubleshoot TLS connectivity to a service endpoint, not the Kubernetes API server, causing the rule to fire despite benign intent.

### Response and remediation

- Immediately delete the affected pod to terminate interactive access, and apply a temporary NetworkPolicy in its namespace that blocks egress to the default/kubernetes service (API server) while you patch its ServiceAccount to set automountServiceAccountToken: false.
- Use API server audit logs and kubectl to enumerate actions taken by the pod’s ServiceAccount and revert any unauthorized objects it created or modified (Pods, CronJobs, RoleBindings, Secrets), and remove any attached ephemeral containers across the namespace.
- Rotate credentials and restore workloads by deleting any legacy ServiceAccount token Secret, restarting pods to issue new bound tokens, rebuilding the image from a trusted base, and redeploying with read-only rootfs and minimal RBAC verified via kubectl auth can-i.
- Escalate to incident response if audit logs show Secrets access or create/patch/update on workloads, if the ServiceAccount holds cluster-admin, or if the observed commands used curl -k/--insecure, wget --no-check-certificate, or openssl/socat/ncat with SSL to the API server.
- Harden the cluster by enforcing admission controls that deny kubectl exec/attach for non-admins, requiring automountServiceAccountToken: false by default and short-lived bound tokens where needed, restricting NetworkPolicies so only designated controllers can reach the API server, and adopting distroless images that omit curl/wget/openssl/ncat.

