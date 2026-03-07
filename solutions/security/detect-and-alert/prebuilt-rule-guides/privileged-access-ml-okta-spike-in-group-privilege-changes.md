---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Group Privilege Change Events" prebuilt detection rule.
---

# Spike in Group Privilege Change Events

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Group Privilege Change Events

In environments using Okta, group privilege changes are crucial for managing access. Adversaries may exploit this by adding themselves to privileged groups, gaining unauthorized access. The detection rule leverages machine learning to identify unusual spikes in these events, signaling potential privilege escalation attempts, thus aiding in early threat detection and response.

### Possible investigation steps

- Review the specific group privilege change events identified by the machine learning job to determine which accounts were added to privileged groups.
- Cross-reference the accounts involved in the privilege changes with recent login activity to identify any unusual or suspicious access patterns.
- Check the history of privilege changes for the affected groups to see if there is a pattern of unauthorized access or if this is an isolated incident.
- Investigate the source IP addresses and locations associated with the privilege change events to identify any anomalies or unexpected geolocations.
- Examine any recent changes to the accounts involved, such as password resets or multi-factor authentication (MFA) modifications, to assess if they have been compromised.
- Collaborate with the affected users or their managers to verify if the privilege changes were authorized and legitimate.

### False positive analysis

- Routine administrative tasks may trigger spikes in group privilege changes. Regularly scheduled audits or updates to group memberships should be documented and excluded from alerts.
- Automated scripts or tools that manage user access can cause frequent changes. Identify these scripts and create exceptions for their activity to prevent false positives.
- Organizational restructuring or mergers often lead to bulk updates in group privileges. During these periods, temporarily adjust the sensitivity of the detection rule or whitelist specific activities.
- Onboarding or offboarding processes can result in a high volume of legitimate group changes. Coordinate with HR and IT to anticipate these events and adjust monitoring accordingly.
- Changes in security policies or compliance requirements might necessitate widespread privilege adjustments. Ensure these policy-driven changes are communicated to the security team to avoid unnecessary alerts.

### Response and remediation

- Immediately isolate the affected accounts by removing them from any high-privilege groups to prevent further unauthorized access.
- Conduct a thorough review of recent group membership changes in Okta to identify any other unauthorized privilege escalations.
- Reset passwords and enforce multi-factor authentication for the affected accounts to secure them against further compromise.
- Notify the security team and relevant stakeholders about the incident for awareness and potential escalation if further suspicious activity is detected.
- Implement additional monitoring on the affected accounts and privileged groups to detect any further unauthorized changes or access attempts.
- Review and update access control policies to ensure that only authorized personnel can modify group memberships, reducing the risk of future privilege escalation.
- Document the incident, including all actions taken, to improve response strategies and inform future security measures.
