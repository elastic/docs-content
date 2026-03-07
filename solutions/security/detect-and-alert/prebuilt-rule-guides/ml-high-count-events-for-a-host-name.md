---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Spike in host-based traffic" prebuilt detection rule.
---

# Spike in host-based traffic

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in host-based traffic
The detection of a spike in host-based traffic leverages machine learning to identify anomalies in network behavior, which may indicate security threats like DDoS attacks or data exfiltration. Adversaries exploit this by overwhelming systems or stealthily transferring data. The rule, with a low severity score, flags unusual traffic patterns, enabling analysts to investigate potential compromises or misconfigurations.

### Possible investigation steps

- Review the timestamp and source of the traffic spike to determine the exact time and origin of the anomaly.
- Analyze the affected host's network logs to identify any unusual outbound or inbound connections that coincide with the spike.
- Check for any recent changes or updates on the affected host that might have triggered the spike, such as software installations or configuration changes.
- Investigate any associated user accounts for signs of unauthorized access or privilege escalation activities.
- Correlate the spike with other security alerts or logs to identify potential patterns or related incidents.
- Assess the host for signs of malware infection or indicators of compromise that could explain the abnormal traffic behavior.

### False positive analysis

- Routine software updates or patch management activities can cause temporary spikes in host-based traffic. Users should monitor scheduled update times and create exceptions for these periods to avoid false positives.
- Backup operations often generate increased network traffic. Identifying and excluding these regular backup windows from monitoring can help reduce false alerts.
- High-volume data transfers within the organization, such as large file uploads or downloads for legitimate business purposes, may trigger the rule. Establishing baseline traffic patterns for these activities and setting exceptions can mitigate unnecessary alerts.
- Automated scripts or batch processes that run at specific times and generate predictable traffic spikes should be documented and excluded from anomaly detection to prevent false positives.
- Internal network scans or vulnerability assessments conducted by IT security teams can mimic malicious traffic patterns. These should be scheduled and whitelisted to avoid triggering the rule.

### Response and remediation

- Isolate the affected host from the network to prevent further data exfiltration or participation in a DDoS attack.
- Conduct a thorough scan of the isolated host for malware or unauthorized software, and remove any malicious files or applications found.
- Review and reset credentials for any accounts that may have been compromised, ensuring that privilege escalation is mitigated.
- Monitor network traffic for any additional anomalies or spikes that could indicate further compromise or ongoing attacks.
- Restore the affected host from a known good backup if malware or significant unauthorized changes are detected.
- Implement network segmentation to limit the spread of potential threats and reduce the impact of similar incidents in the future.
- Escalate the incident to the security operations center (SOC) or relevant team for further analysis and to determine if additional resources are needed for a comprehensive response.
