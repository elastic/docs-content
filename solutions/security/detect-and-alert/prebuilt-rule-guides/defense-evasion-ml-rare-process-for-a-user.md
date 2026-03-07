---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Process Spawned by a User" prebuilt detection rule.
---

# Unusual Process Spawned by a User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Process Spawned by a User

The detection of unusual processes spawned by users leverages machine learning to identify anomalies in user behavior and process execution. Adversaries often exploit legitimate tools, known as LOLbins, to evade detection. This rule uses both supervised and unsupervised ML models to flag processes that deviate from typical user activity, indicating potential misuse or masquerading tactics.

### Possible investigation steps

- Review the user context associated with the alert to determine if the user has a history of spawning unusual processes or if this is an isolated incident.
- Examine the specific process flagged by the alert, including its command line arguments, parent process, and any associated network activity, to identify potential indicators of compromise.
- Check for the presence of known LOLbins or other legitimate tools that may have been exploited, as indicated by the alert's focus on defense evasion tactics.
- Investigate any recent changes in the user's behavior or system configuration that could explain the anomaly, such as software updates or new application installations.
- Correlate the alert with other security events or logs from the same timeframe to identify any related suspicious activities or patterns.
- Assess the risk score and severity level in the context of the organization's threat landscape to prioritize the response and determine if further action is needed.

### False positive analysis

- Legitimate administrative tools may trigger false positives if they are used in atypical contexts. Users should review the context of the process execution and, if deemed safe, add these tools to an exception list to prevent future alerts.
- Scheduled tasks or scripts that run infrequently might be flagged as unusual. Verify the legitimacy of these tasks and consider excluding them if they are part of regular maintenance or updates.
- Software updates or installations can spawn processes that appear anomalous. Confirm the source and purpose of these updates, and if they are routine, create exceptions for these specific processes.
- Developers or IT personnel using command-line tools for legitimate purposes may trigger alerts. Evaluate the necessity of these tools in their workflow and whitelist them if they are consistently used in a non-malicious manner.
- New or infrequently used applications might be flagged due to lack of historical data. Assess the application's legitimacy and, if appropriate, add it to a list of known safe applications to reduce false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further spread or communication with potential command and control servers.
- Terminate the suspicious process identified by the alert to halt any ongoing malicious activity.
- Conduct a thorough review of the user's recent activity and access logs to identify any unauthorized actions or data access.
- Reset the credentials of the affected user account to prevent further unauthorized access, ensuring that strong, unique passwords are used.
- Scan the system for additional indicators of compromise, such as other unusual processes or modifications to system files, and remove any identified threats.
- Restore the system from a known good backup if any critical system files or configurations have been altered.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
