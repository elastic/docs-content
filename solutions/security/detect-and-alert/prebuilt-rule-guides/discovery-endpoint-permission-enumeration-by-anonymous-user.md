---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kubernetes Potential Endpoint Permission Enumeration Attempt by Anonymous User Detected" prebuilt detection rule.'
---

# Kubernetes Potential Endpoint Permission Enumeration Attempt by Anonymous User Detected

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubernetes Potential Endpoint Permission Enumeration Attempt by Anonymous User Detected

This detects a burst of Kubernetes API requests from an unauthenticated identity that probes many different endpoints and resource types, producing mostly forbidden/unauthorized/not found responses within a small window. It matters because this pattern maps the cluster’s exposed surface and reveals which APIs might be reachable before an attacker commits to credential theft or exploitation. A common usage pattern is scripted GET/LIST sweeps across core and custom resources (for example pods, secrets, namespaces, and CRDs) from one source IP and user agent.

### Possible investigation steps

- Review the specific request URIs and resource types queried and their sequence to fingerprint common reconnaissance tooling and whether high-value endpoints (e.g., secrets, tokenreviews, subjectaccessreviews, CRDs) were probed.  
- Determine whether the apparent source IP is internal or Internet-routable and confirm the true originating client by correlating load balancer/ingress/firewall logs (including X-Forwarded-For) with the audit event timestamps.  
- Validate Kubernetes API server authentication/authorization posture during the window to identify misconfiguration that permits anonymous access and confirm whether any requests returned successful responses that indicate real data exposure.  
- Hunt for follow-on activity from the same origin or user agent such as authenticated requests, service account token usage, RBAC/ClusterRoleBinding changes, pod exec, or secret/configmap reads to assess escalation beyond discovery.  
- If the API endpoint is publicly reachable, apply immediate containment by restricting network access to the API server (allowlisting, VPN/private endpoint, temporary IP blocks) while preserving relevant audit and network logs for forensics.

### False positive analysis

- Misconfigured or transitional API server authentication (e.g., anonymous auth briefly enabled or a failing authn proxy/fronting component) can cause legitimate clients to appear as `system:anonymous` and generate multiple 401/403/404 responses across several endpoints during normal cluster access attempts.
- Internal cluster health checks or component discovery behavior that hits multiple API paths without presenting credentials (or uses requests that the audit log records with empty/null usernames) can resemble enumeration when it produces a short burst of failed requests across diverse resources from a single source IP and user agent.

### Response and remediation

- Immediately restrict Kubernetes API server network exposure by allowlisting known admin/VPN IPs and temporarily blocking the observed source IP(s) and user agent at the load balancer/firewall while preserving audit logs and reverse-proxy access logs for the timeframe.  
- Eradicate the anonymous access path by disabling anonymous authentication on the API server, fixing any misconfigured auth proxy that forwards unauthenticated traffic, and removing any RBAC bindings that grant permissions to `system:anonymous` or `system:unauthenticated`.  
- Validate whether any requests from the same source returned successful responses (especially reads of secrets/configmaps, tokenreviews/subjectaccessreviews, or CRDs) and, if so, rotate impacted service account tokens and credentials and perform a targeted review of recently issued tokens and new ClusterRoleBindings.  
- Recover by re-enabling API access in a controlled manner (private endpoint/VPN, bastion, or mTLS), confirming expected kubectl and controller functionality, and monitoring for renewed bursts of failed requests across many request URIs from unauthenticated identities.  
- Escalate to the incident response lead and platform security team if any anonymous request succeeded, if the probing repeats from multiple external IPs, or if follow-on activity appears (new privileged RBAC, pod exec, or secret reads) within 24 hours of the enumeration attempt.  
- Harden by enforcing least-privilege RBAC, enabling and retaining full audit logging for authn/authz failures, applying API server rate limits/WAF rules for repeated 401/403/404 sweeps, and continuously validating that the API endpoint is not publicly reachable.
