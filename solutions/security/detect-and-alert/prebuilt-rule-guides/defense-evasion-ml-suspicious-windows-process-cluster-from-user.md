---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "User Detected with Suspicious Windows Process(es)" prebuilt detection rule.
---

# User Detected with Suspicious Windows Process(es)

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating User Detected with Suspicious Windows Process(es)

The detection leverages machine learning to identify clusters of Windows processes with high malicious probability, often linked to tactics like masquerading. Adversaries exploit legitimate tools (LOLBins) to evade detection. This rule uses both supervised and unsupervised ML models to flag unusual process clusters, focusing on user-associated anomalies to uncover potential threats.

### Possible investigation steps

- Review the list of processes flagged by the alert to identify any known legitimate applications or tools that might have been misclassified.
- Investigate the user account associated with the suspicious process cluster to determine if there is any history of unusual activity or if the account has been compromised.
- Examine the parent-child relationship of the processes to understand the execution chain and identify any potential masquerading attempts or use of LOLBins.
- Check for any recent changes or updates to the system that might explain the unusual process behavior, such as software installations or updates.
- Correlate the detected processes with any known indicators of compromise (IOCs) or threat intelligence feeds to assess if they are linked to known malicious activity.
- Analyze the network activity associated with the processes to identify any suspicious outbound connections or data exfiltration attempts.

### False positive analysis

- Legitimate administrative tools like PowerShell or Windows Management Instrumentation (WMI) may trigger false positives due to their frequent use in system management. Users can create exceptions for these tools when used by trusted administrators.
- Software updates or installations often involve processes that mimic suspicious behavior. Exclude these processes by identifying and whitelisting update-related activities from known software vendors.
- Automated scripts or scheduled tasks that perform routine maintenance can be misclassified as malicious. Review and whitelist these tasks if they are part of regular system operations.
- Development environments may spawn multiple processes that resemble malicious clusters. Developers should document and exclude these processes when they are part of legitimate development activities.
- Security software or monitoring tools might generate process clusters that appear suspicious. Ensure these tools are recognized and excluded from analysis to prevent false alerts.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of potential malicious activity.
- Terminate the suspicious processes identified by the alert to halt any ongoing malicious actions.
- Conduct a thorough review of the affected user's account for any unauthorized access or changes, and reset credentials if necessary.
- Analyze the use of any identified LOLBins to determine if they were used maliciously and restrict their execution through application whitelisting or policy adjustments.
- Collect and preserve relevant logs and forensic data from the affected system for further analysis and to aid in understanding the scope of the incident.
- Escalate the incident to the security operations center (SOC) or incident response team for a deeper investigation and to determine if additional systems are compromised.
- Implement enhanced monitoring and detection rules to identify similar patterns of behavior in the future, focusing on the specific tactics and techniques used in this incident.
