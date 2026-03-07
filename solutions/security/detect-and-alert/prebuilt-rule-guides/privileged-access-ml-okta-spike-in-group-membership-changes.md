---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Spike in Group Membership Events" prebuilt detection rule.'
---

# Spike in Group Membership Events

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Group Membership Events

In modern IT environments, group membership management is crucial for controlling access to resources. Adversaries may exploit this by adding accounts to privileged groups, thereby escalating their access rights. The detection rule leverages machine learning to identify unusual spikes in group membership events, signaling potential unauthorized access attempts. This proactive approach helps in mitigating risks associated with privilege escalation.

### Possible investigation steps

- Review the specific Okta group membership events that triggered the alert to identify which accounts were added to privileged groups.
- Cross-reference the accounts added with known user roles and responsibilities to determine if the changes align with expected access patterns.
- Check recent activity logs for the accounts added to privileged groups to identify any suspicious or unauthorized actions following the group membership change.
- Investigate the source of the group membership changes, including the user or system that initiated the changes, to assess if it was a legitimate administrative action.
- Analyze historical data for similar spikes in group membership events to determine if this is part of a recurring pattern or an isolated incident.
- Consult with the IT or security team to verify if there were any recent changes in access policies or group management procedures that could explain the spike.

### False positive analysis

- Routine administrative tasks may trigger spikes in group membership events, such as scheduled updates or onboarding processes. Users can create exceptions for these known activities to prevent false alerts.
- Automated scripts or tools that manage group memberships for legitimate purposes might cause false positives. Identifying and excluding these scripts from monitoring can reduce unnecessary alerts.
- Changes in group membership due to organizational restructuring or policy updates can appear as spikes. Documenting these changes and adjusting the detection parameters accordingly can help mitigate false positives.
- Frequent legitimate access requests to privileged groups during specific business cycles, like end-of-quarter financial reviews, can be excluded by setting time-based exceptions.
- Regular audits or compliance checks that involve temporary access to privileged groups should be accounted for by creating temporary exceptions during these periods.

### Response and remediation

- Immediately isolate the affected accounts by removing them from any privileged groups to prevent further unauthorized access.
- Conduct a thorough review of recent group membership changes in Okta to identify any other unauthorized additions and remove them as necessary.
- Reset passwords and enforce multi-factor authentication for the affected accounts to secure them against further compromise.
- Notify the security operations team and relevant stakeholders about the incident for awareness and further investigation.
- Implement additional monitoring on the affected accounts and privileged groups to detect any further suspicious activity.
- Review and update access control policies to ensure that only authorized personnel can modify group memberships, reducing the risk of future unauthorized changes.
- Document the incident and response actions taken, and conduct a post-incident review to identify any gaps in the current security posture and improve future response efforts.
