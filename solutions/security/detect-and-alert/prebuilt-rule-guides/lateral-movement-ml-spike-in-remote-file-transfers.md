---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in Remote File Transfers" prebuilt detection rule.
---

# Spike in Remote File Transfers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Remote File Transfers

Remote file transfer technologies facilitate data sharing across networks, essential for collaboration and operations. However, adversaries exploit these to move laterally within a network, often transferring data stealthily to avoid detection. The 'Spike in Remote File Transfers' detection rule leverages machine learning to identify unusual transfer volumes, signaling potential malicious activity by comparing against established network baselines.

### Possible investigation steps

- Review the alert details to identify the specific host and time frame associated with the abnormal file transfer activity.
- Analyze network logs and remote file transfer logs to determine the source and destination of the transfers, focusing on any unusual or unauthorized endpoints.
- Cross-reference the identified host with known assets and user accounts to verify if the activity aligns with expected behavior or if it involves unauthorized access.
- Investigate any associated user accounts for signs of compromise, such as unusual login times or locations, by reviewing authentication logs.
- Check for any recent changes or anomalies in the network baseline that could explain the spike in file transfers, such as new software deployments or legitimate large data migrations.
- Correlate the detected activity with other security alerts or incidents to identify potential patterns or coordinated attacks within the network.

### False positive analysis

- Regularly scheduled data backups or synchronization tasks can trigger false positives. Identify these tasks and create exceptions to prevent them from being flagged.
- Automated software updates or patch management systems may cause spikes in file transfers. Exclude these systems from the rule to reduce false alerts.
- Internal data sharing between departments for legitimate business purposes might be misidentified. Establish a baseline for these activities and adjust the detection thresholds accordingly.
- High-volume data transfers during specific business operations, such as end-of-month reporting, can be mistaken for malicious activity. Temporarily adjust the rule settings during these periods to accommodate expected increases in transfer volumes.
- Frequent file transfers from trusted external partners or vendors should be monitored and, if consistently benign, added to an allowlist to minimize unnecessary alerts.

### Response and remediation

- Isolate the affected host immediately to prevent further lateral movement and potential data exfiltration. Disconnect it from the network to contain the threat.
- Conduct a thorough analysis of the transferred files to determine if sensitive data was involved and assess the potential impact of the data exposure.
- Review and terminate any unauthorized remote access sessions or services on the affected host to prevent further exploitation.
- Reset credentials for any accounts that were used or potentially compromised during the incident to prevent unauthorized access.
- Apply security patches and updates to the affected systems to address any vulnerabilities that may have been exploited by the attackers.
- Monitor network traffic for any additional unusual remote file transfer activities, using enhanced logging and alerting to detect similar threats in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to ensure comprehensive remediation efforts are undertaken.
