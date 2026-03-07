---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Group Application Assignment Change Events" prebuilt detection rule.
---

# Spike in Group Application Assignment Change Events

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Group Application Assignment Change Events

In modern environments, identity and access management systems like Okta manage user access to applications. Adversaries may exploit these systems by altering group application assignments to gain unauthorized access or escalate privileges. The detection rule leverages machine learning to identify unusual spikes in these changes, signaling potential misuse and enabling timely investigation of privilege escalation activities.

### Possible investigation steps

- Review the specific group application assignment change events that triggered the alert to identify which groups and applications were involved.
- Analyze the timeline of the changes to determine if there is a pattern or specific time frame when the spike occurred.
- Investigate the user accounts associated with the changes to assess if they have a history of suspicious activity or if they belong to high-risk roles.
- Check for any recent changes in group membership or application access policies that could explain the spike in assignment changes.
- Correlate the events with other security alerts or logs to identify any concurrent suspicious activities, such as failed login attempts or unusual access patterns.
- Consult with the IT or security team to verify if there were any legitimate administrative activities or changes that could have caused the spike.

### False positive analysis

- Routine administrative changes in group application assignments can trigger false positives. Regularly review and document these changes to differentiate them from suspicious activities.
- Automated processes or scripts that frequently update group assignments may cause spikes. Identify and whitelist these processes to prevent unnecessary alerts.
- Organizational restructuring or onboarding/offboarding activities can lead to increased group assignment changes. Temporarily adjust the detection thresholds or exclude these events during known periods of high activity.
- Changes related to application updates or migrations might be flagged. Coordinate with IT teams to schedule these changes and exclude them from monitoring during the update window.
- Frequent changes by trusted users or administrators can be excluded by creating exceptions for specific user accounts or roles, ensuring that only unexpected changes trigger alerts.

### Response and remediation

- Immediately isolate affected user accounts and groups to prevent further unauthorized access or privilege escalation.
- Revert any unauthorized group application assignments to their previous state to mitigate potential misuse.
- Conduct a thorough review of recent changes in group application assignments to identify any additional unauthorized modifications.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if additional systems or accounts have been compromised.
- Implement additional monitoring on the affected accounts and groups to detect any further suspicious activity.
- Review and update access controls and group assignment policies to prevent similar unauthorized changes in the future.
- Coordinate with the IT and security teams to ensure that all affected systems and applications are patched and secured against known vulnerabilities.
