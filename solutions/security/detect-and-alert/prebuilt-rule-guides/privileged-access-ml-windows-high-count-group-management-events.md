---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Group Management Events" prebuilt detection rule.
---

# Spike in Group Management Events

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Group Management Events

The detection of spikes in group management events leverages machine learning to monitor and identify unusual patterns in user activities related to group memberships. Adversaries may exploit this by adding or removing users from privileged groups to escalate privileges or alter access controls. The detection rule identifies these anomalies, flagging potential unauthorized modifications indicative of privilege escalation attempts.

### Possible investigation steps

- Review the specific user account associated with the spike in group management events to determine if the activity aligns with their typical behavior or role.
- Check the timeline of the group management events to identify any patterns or sequences that might suggest unauthorized access or privilege escalation attempts.
- Investigate the source IP addresses and devices used during the group management events to verify if they are consistent with the user's usual access points or if they indicate potential compromise.
- Examine recent changes to privileged groups, focusing on additions or removals of users, to assess if these modifications were authorized and necessary.
- Cross-reference the flagged events with any recent support tickets or change requests to confirm if the actions were legitimate and documented.
- Look for any other related alerts or anomalies in the same timeframe that might indicate a broader security incident or coordinated attack.

### False positive analysis

- Routine administrative tasks can trigger spikes in group management events, such as scheduled user onboarding or offboarding. To manage this, create exceptions for known periods of increased activity.
- Automated scripts or tools that manage group memberships might cause false positives. Identify these scripts and exclude their activities from the rule's monitoring.
- Changes in organizational structure, like department mergers, can lead to legitimate spikes. Document these changes and adjust the rule's sensitivity temporarily.
- Regular audits or compliance checks that involve group membership reviews may appear as anomalies. Schedule these activities and inform the monitoring team to prevent false alerts.
- High turnover rates in certain departments can result in frequent group changes. Monitor these departments separately and adjust thresholds accordingly.

### Response and remediation

- Immediately isolate the affected user account by disabling it to prevent further unauthorized group management activities.
- Review and audit recent changes to group memberships, focusing on privileged groups, to identify any unauthorized additions or removals.
- Revert any unauthorized changes to group memberships to restore the intended access controls.
- Conduct a thorough investigation to determine the source of the anomaly, including checking for compromised credentials or insider threats.
- Reset the password for the affected user account and enforce multi-factor authentication to enhance security.
- Notify the security operations team and relevant stakeholders about the incident for awareness and further investigation.
- Implement additional monitoring on the affected account and related privileged groups to detect any further suspicious activities.
