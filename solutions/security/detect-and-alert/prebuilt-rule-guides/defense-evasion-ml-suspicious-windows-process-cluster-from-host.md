---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Host Detected with Suspicious Windows Process(es)" prebuilt detection rule.'
---

# Host Detected with Suspicious Windows Process(es)

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Host Detected with Suspicious Windows Process(es)

The detection leverages machine learning to identify clusters of Windows processes with high malicious probability scores. Adversaries exploit legitimate tools, known as LOLbins, to evade detection. This rule uses both supervised and unsupervised ML models to flag unusual process clusters on a single host, indicating potential masquerading tactics for defense evasion.

### Possible investigation steps

- Review the host name associated with the suspicious process cluster to determine if it is a critical asset or has a history of similar alerts.
- Examine the specific processes flagged by the ProblemChild supervised ML model to identify any known LOLbins or unusual command-line arguments that may indicate masquerading.
- Check the timeline of the process execution to see if it coincides with any known scheduled tasks or user activity that could explain the anomaly.
- Investigate the parent-child relationship of the processes to identify any unexpected or unauthorized process spawning patterns.
- Correlate the alert with other security events or logs from the same host to identify any additional indicators of compromise or related suspicious activity.
- Assess the network activity associated with the host during the time of the alert to detect any potential data exfiltration or communication with known malicious IP addresses.

### False positive analysis

- Legitimate administrative tools like PowerShell or Windows Management Instrumentation (WMI) may be flagged as suspicious due to their dual-use nature. Users can create exceptions for these tools when used by trusted administrators or during scheduled maintenance.
- Automated scripts or scheduled tasks that perform routine system checks or updates might trigger alerts. Review these processes and whitelist them if they are verified as part of regular operations.
- Software updates or installations that involve multiple processes spawning in a short time frame can be mistaken for malicious clusters. Ensure that these activities are documented and create exceptions for known update processes.
- Development or testing environments where new or experimental software is frequently executed may generate false positives. Consider excluding these environments from monitoring or adjusting the sensitivity of the rule for these specific hosts.
- Frequent use of remote desktop or remote management tools by IT staff can appear suspicious. Implement user-based exceptions for known IT personnel to reduce unnecessary alerts.

### Response and remediation

- Isolate the affected host immediately to prevent further spread of potential malicious activity. Disconnect it from the network to contain the threat.
- Terminate the suspicious processes identified by the alert. Use task management tools or scripts to ensure all instances of the processes are stopped.
- Conduct a thorough review of the host's system logs and process history to identify any additional indicators of compromise or related malicious activity.
- Restore the host from a known good backup if available, ensuring that the backup is free from any signs of compromise.
- Update and patch the host's operating system and all installed software to close any vulnerabilities that may have been exploited.
- Implement application whitelisting to prevent unauthorized or suspicious processes from executing in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional hosts are affected.
