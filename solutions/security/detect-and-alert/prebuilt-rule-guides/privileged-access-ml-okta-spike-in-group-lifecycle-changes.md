---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Spike in Group Lifecycle Change Events" prebuilt detection rule.'
---

# Spike in Group Lifecycle Change Events

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Group Lifecycle Change Events

In identity management systems like Okta, group lifecycle changes are crucial for managing user access and permissions. Adversaries may exploit these changes to escalate privileges or maintain unauthorized access. The detection rule leverages machine learning to identify unusual spikes in these events, signaling potential misuse. By focusing on privilege escalation tactics, it helps security analysts pinpoint and investigate suspicious activities.

### Possible investigation steps

- Review the specific group lifecycle change events that triggered the alert to identify which groups were altered and the nature of the changes.
- Examine the user accounts associated with the changes to determine if they have a history of suspicious activity or if they have recently been granted elevated privileges.
- Check the timestamps of the group changes to see if they coincide with other unusual activities or known attack patterns within the organization.
- Investigate any recent access requests or approvals related to the affected groups to ensure they were legitimate and authorized.
- Correlate the group changes with other security alerts or logs to identify potential lateral movement or privilege escalation attempts by adversaries.
- Assess the current membership of the affected groups to ensure no unauthorized users have been added or legitimate users removed.

### False positive analysis

- Routine administrative changes in group memberships can trigger false positives. Security teams should identify and whitelist these regular activities to prevent unnecessary alerts.
- Automated processes or scripts that modify group structures for legitimate reasons may cause spikes. Exclude these known processes by creating exceptions in the detection rule.
- Large-scale onboarding or offboarding events can lead to a temporary increase in group lifecycle changes. Coordinate with HR or relevant departments to anticipate these events and adjust monitoring thresholds accordingly.
- Changes due to system integrations or updates might be misinterpreted as suspicious. Document and exclude these events by maintaining an updated list of integration activities.
- Regular audits or compliance checks that involve group modifications should be recognized and filtered out to avoid false alarms.

### Response and remediation

- Immediately isolate affected user accounts and groups to prevent further unauthorized access or privilege escalation. This can be done by temporarily disabling accounts or removing them from critical groups.
- Conduct a thorough review of recent group lifecycle changes to identify unauthorized modifications. Revert any unauthorized changes to restore the original group structures and permissions.
- Implement additional monitoring on the affected accounts and groups to detect any further suspicious activities. This includes setting up alerts for any new group changes or access attempts.
- Escalate the incident to the security operations team for a deeper investigation into potential lateral movement or persistence mechanisms used by the adversary.
- Review and update access controls and group management policies to ensure they align with the principle of least privilege, minimizing the risk of privilege escalation.
- Coordinate with the IT and security teams to apply patches or updates to any vulnerabilities identified during the investigation that may have been exploited for privilege escalation.
- Document the incident, including all actions taken, and conduct a post-incident review to identify lessons learned and improve future response strategies.
