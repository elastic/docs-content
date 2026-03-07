---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Special Privilege Use Events" prebuilt detection rule.
---

# Spike in Special Privilege Use Events

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Special Privilege Use Events

Machine learning models monitor special privilege use, identifying anomalies that suggest unauthorized access. Adversaries exploit these privileges to escalate access, execute unauthorized actions, or maintain system persistence. The detection rule leverages ML to spot unusual spikes in privileged operations, flagging potential misuse for further investigation.

### Possible investigation steps

- Review the user account associated with the spike in special privilege use events to determine if the activity aligns with their normal behavior or job role.
- Examine the specific privileged operations and service calls that were flagged to identify any unusual or unauthorized actions.
- Check for any recent changes in user permissions or group memberships that could explain the increase in privilege use.
- Investigate any corresponding logs or alerts around the same timeframe to identify potential indicators of compromise or related suspicious activities.
- Assess the system or application where the privilege escalation occurred for any signs of exploitation or unauthorized access attempts.
- Correlate the detected spike with known threat intelligence or recent security advisories to determine if it matches any known attack patterns or vulnerabilities.

### False positive analysis

- Routine administrative tasks by IT personnel can trigger false positives. Regularly review and whitelist known administrative accounts to prevent unnecessary alerts.
- Scheduled maintenance activities often involve elevated privileges. Document and exclude these activities from monitoring during known maintenance windows.
- Automated scripts or services that require elevated privileges may cause spikes. Identify and exclude these scripts or services from the rule to reduce false positives.
- Software updates or installations can lead to temporary spikes in privilege use. Coordinate with IT to recognize these events and adjust monitoring rules accordingly.
- Frequent legitimate use of privileged operations by certain users or roles should be analyzed. Establish a baseline for these users and adjust the detection threshold to accommodate their normal activity levels.

### Response and remediation

- Immediately isolate the affected user account to prevent further unauthorized privileged operations. Disable the account or change its credentials to stop potential misuse.
- Conduct a thorough review of recent privileged operations and service calls associated with the user account to identify any unauthorized actions or changes made during the spike.
- Revoke any unnecessary privileges or access rights from the affected user account to minimize the risk of future exploitation.
- Implement additional monitoring on the affected system and user account to detect any further suspicious activities or attempts to regain unauthorized access.
- Escalate the incident to the security operations team for a deeper investigation into potential privilege escalation techniques used, referencing MITRE ATT&CK technique T1068.
- Review and update access control policies and privilege management practices to ensure they align with the principle of least privilege, reducing the risk of similar incidents.
- Conduct a post-incident analysis to identify any gaps in detection or response and enhance the machine learning model's ability to detect similar threats in the future.
