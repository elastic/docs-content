---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kubernetes Potential Endpoint Permission Enumeration Attempt Detected" prebuilt detection rule.
---

# Kubernetes Potential Endpoint Permission Enumeration Attempt Detected

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubernetes Potential Endpoint Permission Enumeration Attempt Detected

Detects a single Kubernetes identity from one IP issuing a burst of API calls across many resources and URLs with a mix of allowed and denied outcomes, consistent with automated RBAC probing rather than normal operations. This matters because attackers use it to map what they can access and identify high-value objects (secrets, pods, nodes) before escalation or lateral movement. A common pattern is running a script that iterates list/get/watch on dozens of API endpoints until it finds ones that return data.

### Possible investigation steps

- Expand the timeline around the alert for the same identity and source to reconstruct the full API-call sequence and identify which resource types returned successful data, prioritizing secrets, configmaps, nodes, pods, and RBAC objects.  
- Determine whether the source IP maps to a cluster node, pod egress/NAT, VPN, or an external host using infrastructure and network telemetry, and confirm it matches expected administrative or automation origins.  
- Validate whether the acting identity is a human user, service account, or external auth integration and review recent sign-ins/token issuance and current RBAC bindings for unexpected or overly broad access.  
- Hunt for follow-on actions from the same identity or IP that indicate escalation or execution, such as modifying role bindings, creating privileged pods, accessing secret data, or initiating exec/port-forward operations.  
- If the activity is not clearly legitimate, contain by rotating or disabling the credential and tightening permissions, then search for the same enumeration behavior across other identities and sources to scope impact.

### False positive analysis

- A cluster administrator or platform engineer using kubectl from a single workstation/VPN IP to troubleshoot RBAC issues may rapidly test get/list/watch across multiple resources and endpoints, producing a mix of allowed and forbidden responses within a short window.  
- A newly deployed or updated in-cluster component using a service account may probe several Kubernetes API resources during initialization or capability detection and encounter intermittent authorization denials due to incomplete RBAC bindings, generating diverse requestURIs/resources with both success and failure outcomes.

### Response and remediation

- Quarantine the actor by disabling the implicated user or service account (revoke kubeconfig/token and delete associated Secrets for service-account tokens) and, if the source IP is external, block it at the API server ingress/load balancer while preserving access for known admin networks.  
- Eradicate the access path by rotating any credentials the identity could have used (OIDC refresh tokens, client certs, static kubeconfigs) and removing unexpected RBAC RoleBindings/ClusterRoleBindings or groups that grant broad read access discovered during review.  
- Validate impact and recover by reviewing what endpoints returned successful data during the burst (especially secrets, configmaps, nodes, pods, and RBAC objects), rotating any exposed application secrets, and restarting affected workloads after credential updates.  
- Escalate immediately to incident response if the same identity subsequently creates/patches RBAC bindings, deploys privileged pods/daemonsets, performs exec/port-forward, or accesses secret data across multiple namespaces.  
- Harden by enforcing least-privilege RBAC for humans and service accounts, segmenting API access with network controls (private endpoint/VPN allowlists), and enabling short-lived tokens with regular rotation plus alerting on repeated mixed allow/deny probing across many resources.

