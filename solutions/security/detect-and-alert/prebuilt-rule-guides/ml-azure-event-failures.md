---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Azure Activity Logs Failed Messages" prebuilt detection rule.
---

# Spike in Azure Activity Logs Failed Messages

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Azure Activity Logs Failed Messages

This rule flags an unusual surge in failed control‑plane operations recorded in the platform’s activity logs, highlighting abrupt increases in a specific failure type. It matters because concentrated failures frequently accompany probing for privileges, discovery, or staged lateral movement. Adversaries often script through the management API to list subscriptions, role assignments, or policy definitions and then attempt role updates or assignment creations at scale, generating clusters of authorization and scope‑validation failures as they enumerate tenants and test permission boundaries.

### Possible investigation steps

- Categorize the spike by failure reason (authorization, policy, scope validation, throttling, or availability) and pivot to the initiating identities, apps, and source IPs to see whether a single principal or distributed automation is driving it.
- Correlate these failures with Entra ID sign‑in logs and Conditional Access evaluations for the same principals to determine whether authentication, token, or policy blocks explain the surge.
- Review recent RBAC changes (role assignments/definitions), PIM activations, and deny/policy assignments around the spike to spot attempted privilege escalation or scope misconfiguration.
- Map the affected resource providers and scopes (tenant, subscription, resource group) to identify reconnaissance patterns such as wide listing followed by repeated unauthorized write attempts.
- Confirm benign causes such as expired service principal credentials, broken pipelines, or provider outages with owners, and if intent is suspect promptly disable the principal, revoke tokens, and rotate secrets.

### False positive analysis

- Expired or rotated service principal credentials in scheduled automation led to repeated Azure management operations with invalid tokens, spiking AuthorizationFailed entries until the secret was updated.
- A planned rollout of Azure Policy with a deny effect or the application of resource locks temporarily blocked routine deployments across multiple scopes, generating a concentrated burst of failed write operations during the change window.

### Response and remediation

- Temporarily disable the Entra ID service principal or user driving the spike, revoke all refresh/access tokens, and apply a Conditional Access block for management API access from its source IP ranges to halt further control‑plane attempts.
- Pause implicated automation by stopping the Azure DevOps pipeline or Automation Account runbook, invalidate any associated PATs or shared secrets, and rotate the application/client secret or federated credentials tied to the identity.
- Back out unauthorized changes by removing newly created role assignments, deny assignments, or policy assignments introduced during the window, and restore intended RBAC at the affected subscriptions, management groups, and resource groups via IaC state.
- Recover by fixing the misconfiguration or credentials, validating successful test operations (e.g., list and create where permitted) in a non‑production subscription, and then re‑enable automation with least‑privilege scopes while monitoring for a return to normal failure rates.
- Escalate to the incident response lead if failures include repeated attempts to change role assignments or policy at tenant or management‑group scope, originate from unfamiliar geographies or unapproved IP ranges, spread across multiple subscriptions, or persist more than 15 minutes after containment.
- Harden by enforcing PIM for privileged roles, enabling Conditional Access for workload identities and administrators (MFA and named locations), implementing secret scanning and rotation for repos and pipelines, exporting Activity Logs to Log Analytics with retention, and alerting on abnormal management‑plane failures per identity.

