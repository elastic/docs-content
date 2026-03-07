---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Correlated Alerts on Similar User Identities" prebuilt detection rule.'
---

# Correlated Alerts on Similar User Identities

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, analysts should validate findings against their environment and identity architecture.

### Investigating Correlated Alerts on Similar User Identities

This rule identifies alerts from multiple integrations and event categories involving different `user.name` values that may represent the same real-world identity.
An LLM is used to assess string similarity and naming patterns to determine whether multiple user identifiers likely belong to the same person, which may indicate account compromise, credential abuse, or identity misuse across systems.

### Possible investigation steps

- Review the correlated `user.name` values and validate whether they represent naming variations, aliases, or identity mappings.
- Examine the LLM output fields (`verdict`, `confidence`, `summary`) as decision support, not ground truth.
- Analyze the diversity of alert sources, event categories, and detection rules involved.
- Reconstruct the alert timeline to identify potential stages such as initial access, lateral movement, privilege escalation, or persistence.
- Correlate with authentication logs, IAM/SSO telemetry, EDR data, and network logs to identify shared sessions, IPs, devices, or hosts.
- Validate identities against directory services, identity providers, and federation mappings.

### False positive analysis

- Identity format variations across systems (e.g., `first.last`, `flast`, `user@domain`).
- Federated identity mappings between on-prem, cloud, and SaaS platforms.
- Service, automation, and CI/CD accounts with similar naming conventions.
- Separate admin and standard user accounts for the same individual.
- Shared credentials or naming templates in development and test environments.

### Response and remediation

- Temporarily disable or suspend correlated accounts if compromise is suspected.
- Revoke active sessions, tokens, and credentials.
- Investigate access scope, privileges, and lateral movement paths.
- Perform endpoint and identity forensics to identify persistence mechanisms.
- Remediate IAM misconfigurations and federation issues.
- Enhance monitoring for identity correlation, credential misuse, and cross-platform abuse..
