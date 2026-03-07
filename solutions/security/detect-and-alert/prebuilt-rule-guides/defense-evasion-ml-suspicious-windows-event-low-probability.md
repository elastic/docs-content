---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Machine Learning Detected a Suspicious Windows Event with a Low Malicious Probability Score" prebuilt detection rule.
---

# Machine Learning Detected a Suspicious Windows Event with a Low Malicious Probability Score

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Machine Learning Detected a Suspicious Windows Event with a Low Malicious Probability Score

The detection leverages a machine learning model to identify potentially suspicious Windows processes with a low likelihood of being malicious, focusing on defense evasion tactics like masquerading. Adversaries may exploit legitimate processes to bypass security measures. This rule flags such events, excluding known benign patterns, to highlight potential threats for further analysis.

### Possible investigation steps

- Review the process details where the problemchild.prediction is 1 and the prediction_probability is less than or equal to 0.98 to understand why the process was flagged as suspicious.
- Check if the process is listed in the blocklist_label as 1, indicating it has been identified as malicious by the model's blocklist.
- Investigate the command-line arguments of the process to identify any unusual or unexpected patterns, excluding known benign patterns such as those involving "C:\WINDOWS\temp\nessus_*.txt" or "C:\WINDOWS\temp\nessus_*.tmp".
- Correlate the flagged process with other system events or logs to determine if it is part of a larger pattern of suspicious activity, focusing on defense evasion tactics like masquerading.
- Assess the parent process and any child processes spawned by the suspicious process to identify potential lateral movement or further malicious activity.
- Consult threat intelligence sources to see if the process or its associated indicators have been reported in recent threat reports or advisories.

### False positive analysis

- Nessus scan files in the Windows temp directory may trigger false positives. Exclude paths like C:\WINDOWS\temp\nessus_*.txt and C:\WINDOWS\temp\nessus_*.tmp to prevent these benign events from being flagged.
- Legitimate software updates or installations might mimic suspicious behavior. Monitor and document regular update schedules to differentiate between expected and unexpected activities.
- System administration scripts that automate tasks can appear suspicious. Identify and whitelist these scripts if they are part of routine operations to avoid unnecessary alerts.
- Custom in-house applications may not be recognized by the model. Work with IT to catalog these applications and create exceptions where necessary to reduce false positives.
- Regularly review and update the blocklist and exception rules to ensure they reflect the current environment and known benign activities.

### Response and remediation

- Isolate the affected system from the network to prevent potential lateral movement by the adversary exploiting the masquerading technique.
- Terminate the suspicious process identified by the machine learning model to halt any ongoing malicious activity.
- Conduct a thorough review of the process's parent and child processes to identify any additional suspicious activities or related processes that may require termination.
- Restore the system from a known good backup if any malicious activity is confirmed, ensuring that the backup is free from compromise.
- Update and patch the system to the latest security standards to close any vulnerabilities that may have been exploited.
- Implement enhanced monitoring for similar masquerading attempts by adjusting alert thresholds or adding specific indicators of compromise (IOCs) related to the detected event.
- Escalate the incident to the security operations center (SOC) or relevant security team for further analysis and to determine if additional systems are affected.
