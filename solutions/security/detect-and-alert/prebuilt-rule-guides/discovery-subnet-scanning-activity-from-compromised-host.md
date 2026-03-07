---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Subnet Scanning Activity from Compromised Host" prebuilt detection rule.
---

# Potential Subnet Scanning Activity from Compromised Host

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Subnet Scanning Activity from Compromised Host

Subnet scanning is a reconnaissance method used by attackers to map network topology and identify active hosts. Adversaries exploit compromised hosts to perform these scans, seeking vulnerabilities for further attacks. The detection rule identifies such activity by monitoring Linux hosts for numerous connection attempts to different IPs within a short period, indicating potential scanning behavior. This helps in early detection and mitigation of network threats.

### Possible investigation steps

- Review the process executable identified in the alert to determine if it is a known or legitimate application that should be making network connections.
- Examine the destination IP addresses to identify any patterns or known malicious IPs, and check if these IPs are part of the organization's network or external.
- Investigate the specific host (using the agent.id) to assess if there are any signs of compromise, such as unusual processes or unauthorized access.
- Correlate the event timestamp with other logs or alerts to identify any concurrent suspicious activities or anomalies on the host.
- Check for any recent changes or updates on the host that might explain the scanning behavior, such as new software installations or configuration changes.

### False positive analysis

- High-volume legitimate network monitoring tools may trigger the rule. Identify and exclude these tools by adding their process executables to an exception list.
- Automated backup systems that connect to multiple hosts within a short timeframe can be mistaken for scanning activity. Review and exclude these systems by their process executable or agent ID.
- Security software performing routine network health checks might generate false positives. Verify these activities and create exceptions based on the specific process executable involved.
- Internal IT scripts or administrative tasks that involve connecting to numerous hosts for maintenance purposes can trigger alerts. Document these tasks and exclude them by process executable or agent ID.
- Cloud-based services or applications that require frequent connections to various hosts for functionality may appear as scanning. Identify these services and exclude them by their process executable or agent ID.

### Response and remediation

- Isolate the compromised host immediately from the network to prevent further scanning and potential lateral movement by the attacker.
- Terminate any suspicious processes identified by the executable name in the alert to stop ongoing scanning activities.
- Conduct a thorough examination of the compromised host to identify and remove any malware or unauthorized access tools that may have been installed.
- Reset credentials and review access permissions for the compromised host to ensure no unauthorized access persists.
- Update and patch the compromised host and any other vulnerable systems identified during the investigation to close security gaps.
- Monitor network traffic closely for any signs of continued scanning or other suspicious activities from other hosts, indicating potential further compromise.
- Escalate the incident to the security operations center (SOC) or incident response team for a comprehensive investigation and to determine if additional hosts are affected.

