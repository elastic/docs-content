---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Decline in host-based traffic" prebuilt detection rule.
---

# Decline in host-based traffic

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Decline in host-based traffic

Host-based traffic monitoring is crucial for identifying anomalies in network activity. A sudden drop in traffic can indicate issues like system compromise, service failure, or misconfiguration. Adversaries might exploit these situations to evade detection or disrupt services. The 'Decline in host-based traffic' rule leverages machine learning to identify unexpected traffic reductions, signaling potential security threats for further investigation.

### Possible investigation steps

- Review the affected host's recent activity logs to identify any unusual patterns or events that coincide with the drop in traffic.
- Check for any recent changes in network configuration or firewall settings that might have inadvertently caused the traffic decline.
- Investigate the status of critical services on the host to determine if any have failed or been stopped unexpectedly.
- Analyze network traffic data to identify any potential signs of compromise, such as connections to known malicious IP addresses or unusual outbound traffic.
- Consult with system administrators to verify if any maintenance or updates were performed around the time of the traffic drop that could explain the anomaly.

### False positive analysis

- Scheduled maintenance or updates can cause temporary drops in host-based traffic. Users should create exceptions for known maintenance windows to prevent false alerts.
- Network configuration changes, such as firewall rule updates or routing adjustments, might lead to expected traffic reductions. Document and exclude these changes from triggering alerts.
- Temporary service outages due to non-security related issues, like hardware failures or software bugs, can be mistaken for threats. Implement monitoring to distinguish between these and actual security incidents.
- Low-usage periods, such as weekends or holidays, may naturally result in reduced traffic. Adjust the machine learning model to account for these patterns by incorporating historical data.
- Legitimate changes in user behavior, such as remote work policies or shifts in business operations, can affect traffic levels. Regularly update the model to reflect these changes and avoid false positives.

### Response and remediation

- Isolate the affected host from the network to prevent potential lateral movement or further compromise.
- Verify the integrity and functionality of critical services on the affected host to identify any failures or misconfigurations.
- Conduct a thorough malware scan on the isolated host to detect and remove any malicious software.
- Review recent configuration changes on the host and revert any unauthorized or suspicious modifications.
- Restore any affected services from known good backups if service failure is confirmed as the cause.
- Monitor network traffic for any signs of unusual activity or attempts to exploit the situation further.
- Escalate the incident to the security operations team for a deeper forensic analysis and to determine if additional hosts are affected.
