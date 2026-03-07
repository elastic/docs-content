---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Elastic Security External Alerts" prebuilt detection rule.'
---

# Elastic Security External Alerts

## Triage and analysis

### Investigating Elastic Security External Alerts

The Elastic Security integration facilitates transferring security alert data from another Elasticsearch instance to your own, enabling threats to be investigated in a centralized manner.

### Possible investigation steps

- Correlate the alert with recent activity on the affected endpoint to identify any unusual or suspicious behavior patterns.
- Check for any additional alerts or logs related to the same endpoint or user to determine if this is part of a broader attack or isolated incident.
- Investigate the source and destination IP addresses involved in the alert to assess if they are known to be malicious or associated with previous threats.
- Analyze any files or processes flagged in the alert to determine if they are legitimate or potentially malicious, using threat intelligence sources if necessary.
- Consult the Elastic Security investigation guide and resources tagged in the alert for specific guidance on handling similar threats.

### False positive analysis

- Alerts triggered by routine software updates or patches can be false positives. Review the context of the alert to determine if it aligns with scheduled maintenance activities.
- Legitimate administrative tools or scripts may trigger alerts. Identify and whitelist these tools if they are verified as non-threatening.
- Frequent alerts from known safe applications or processes can be excluded by creating exceptions for these specific behaviors in the Elastic Security configuration.
- Network scanning or monitoring tools used by IT teams might be flagged. Ensure these tools are documented and excluded from triggering alerts if they are part of regular operations.
- User behavior that is consistent with their role but triggers alerts should be reviewed. If deemed non-malicious, adjust the rule to exclude these specific user actions.

### Response and remediation

- Isolate the affected endpoint immediately to prevent lateral movement and further compromise within the network.
- Analyze the specific alert details to identify the nature of the threat and any associated indicators of compromise (IOCs).
- Remove or quarantine any malicious files or processes identified by the Elastic Security alert to neutralize the threat.
- Apply relevant security patches or updates to address any exploited vulnerabilities on the affected endpoint.
- Conduct a thorough scan of the network to identify any additional endpoints that may have been compromised or are exhibiting similar behavior.
- Document the incident and escalate to the appropriate security team or management if the threat is part of a larger attack campaign or if additional resources are needed for remediation.
- Review and update endpoint protection policies and configurations to enhance detection and prevention capabilities against similar threats in the future.
