---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Spike in Number of Connections Made to a Destination IP" prebuilt detection rule.'
---

# Spike in Number of Connections Made to a Destination IP

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Spike in Number of Connections Made to a Destination IP

Remote Desktop Protocol (RDP) is crucial for remote management and troubleshooting in IT environments. However, adversaries exploit RDP by using multiple compromised IPs to overwhelm a target, ensuring persistence even if some IPs are blocked. The detection rule leverages machine learning to identify unusual spikes in RDP connections to a single IP, signaling potential lateral movement attempts by attackers.

### Possible investigation steps

- Review the list of source IPs that have established RDP connections to the destination IP to identify any known malicious or suspicious IP addresses.
- Check historical data for the destination IP to determine if it has been targeted in previous attacks or if it is a high-value asset within the network.
- Analyze the timing and frequency of the RDP connections to identify any unusual patterns or spikes that could indicate coordinated activity.
- Investigate the user accounts associated with the RDP connections to ensure they are legitimate and have not been compromised.
- Correlate the detected activity with any other security alerts or logs to identify potential lateral movement or further exploitation attempts within the network.

### False positive analysis

- Routine administrative tasks may trigger false positives if multiple IT staff connect to a server for maintenance. Consider creating exceptions for known administrative IPs.
- Automated scripts or monitoring tools that frequently connect to servers for health checks can cause spikes. Identify and exclude these IPs from the rule.
- Load balancers or proxy servers that aggregate connections from multiple clients might appear as a spike. Exclude these devices from the detection rule.
- Scheduled software updates or deployments that require multiple connections to a server can be mistaken for an attack. Whitelist the IPs involved in these processes.
- Internal network scans or vulnerability assessments conducted by security teams can generate high connection counts. Ensure these activities are recognized and excluded.

### Response and remediation

- Immediately isolate the affected destination IP from the network to prevent further unauthorized RDP connections and potential lateral movement.
- Conduct a thorough review of the logs and network traffic associated with the destination IP to identify all source IPs involved in the spike and assess the scope of the compromise.
- Block all identified malicious source IPs at the firewall or network perimeter to prevent further connections to the destination IP.
- Reset credentials and enforce multi-factor authentication for accounts that were accessed via RDP to mitigate unauthorized access.
- Perform a security assessment of the affected systems to identify any signs of compromise or unauthorized changes, and restore systems from clean backups if necessary.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems or networks are affected.
- Update and enhance monitoring rules to detect similar patterns of unusual RDP connection spikes in the future, ensuring quick identification and response to potential threats.
