---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Rare Azure Activity Logs Event Failures" prebuilt detection rule.
---

# Rare Azure Activity Logs Event Failures

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Rare Azure Activity Logs Event Failures

This rule surfaces statistically rare Azure Activity Logs failures, pointing to control‑plane actions that break from typical patterns and may reflect reconnaissance, privilege changes, or defense evasion. A common attacker sequence is using a newly compromised identity to enumerate subscriptions and resource groups through the management API; repeated access denials during these discovery calls can occur as the adversary maps tenant scope and tests permissions before escalating.

### Possible investigation steps

- Classify the failing operations (discovery vs write/privileged) and tie them to the initiating principal and target scope to gauge intent and blast radius.
- Correlate with Entra ID sign-in telemetry for the same principal around the event window to assess geo/device novelty, MFA state, Conditional Access results, and identity risk flags.
- Check whether the identity recently had role assignments, group membership, PIM elevation, or app consent changes, and whether this is first-time access to the affected subscriptions or resource groups.
- Confirm whether Azure Policy denies, deny assignments, or resource locks explain the failures, and verify whether the principal should legitimately be exempt or granted access.
- If the actor is a service principal or managed identity, review recent credential changes (keys/secrets/certificates), app role assignment grants, and automation pipeline updates that could explain unexpected calls.

### False positive analysis

- A newly deployed automation or audit workflow attempts wide-scope resource discovery using a service principal or managed identity, encountering expected RBAC or policy denials that are rare for that caller.
- Recent governance changes such as Azure Policy deny effects, deny assignments, or resource locks cause routine management operations (e.g., writes or deletes) to start failing, creating an unusual failure pattern until baselines adjust.

### Response and remediation

- Immediately contain the initiating identity by disabling user/service principal sign-in, revoking refresh tokens, and applying a temporary Conditional Access block on Azure management endpoints, while placing deny assignments and resource locks on the impacted subscriptions/resource groups.
- Eradicate potential persistence by removing any newly created role assignments, app consent grants, policy exemptions, or management role changes identified in triage, and rotate keys/secrets/certificates for affected service principals or managed identities.
- Recover business operations by restoring access only to verified identities through PIM approvals, re-enabling known-good automation accounts/runbooks, and validating that expected management operations succeed without further rare failures on the targeted resources.
- Escalate to incident response immediately if rare failures are observed across multiple subscriptions or are followed by a successful privileged action (e.g., new Owner or User Access Administrator assignment, app consent grant, or resource lock removal) or originate from an unfamiliar geo/device, triggering tenant-wide containment.
- Harden going forward by enforcing MFA and Conditional Access (including workload identity policies) for Resource Manager access, restricting service principals to least privilege with certificate-based credentials or workload identity federation, implementing deny assignments/resource locks for crown-jewel resources, and centralizing Activity Logs in SIEM with detections for discovery bursts and denied write attempts.

