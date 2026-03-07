---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Port Scanning Activity from Compromised Host" prebuilt detection rule.
---

# Potential Port Scanning Activity from Compromised Host

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Port Scanning Activity from Compromised Host

Port scanning is a reconnaissance method used by attackers to identify open ports and services on a network, often as a precursor to exploitation. In Linux environments, compromised hosts may perform rapid connection attempts to numerous ports, signaling potential scanning activity. The detection rule identifies such behavior by analyzing network logs for a high number of distinct port connections from a single host within a short timeframe, indicating possible malicious intent.

### Possible investigation steps

- Review the network logs to identify the specific host exhibiting the port scanning behavior by examining the destination.ip and process.executable fields.
- Analyze the @timestamp field to determine the exact time frame of the scanning activity and correlate it with any other suspicious activities or alerts from the same host.
- Investigate the process.executable field to understand which application or service initiated the connection attempts, and verify if it is a legitimate process or potentially malicious.
- Check the destination.port field to identify the range and types of ports targeted by the scanning activity, which may provide insights into the attacker's objectives or the services they are interested in.
- Assess the host's security posture by reviewing recent changes, installed software, and user activity to determine if the host has been compromised or if the scanning is part of legitimate network operations.
- Consult the original documents and logs for additional context and details that may not be captured in the alert to aid in a comprehensive investigation.

### False positive analysis

- Legitimate network scanning tools used by system administrators for network maintenance or security assessments can trigger this rule. To handle this, identify and whitelist the IP addresses or processes associated with these tools.
- Automated vulnerability scanners or monitoring systems that perform regular checks on network services may cause false positives. Exclude these systems by creating exceptions for their known IP addresses or process names.
- High-volume legitimate services that open multiple connections to different ports, such as load balancers or proxy servers, might be flagged. Review and exclude these services by specifying their IP addresses or process executables.
- Development or testing environments where frequent port scanning is part of routine operations can be mistakenly identified. Implement exceptions for these environments by excluding their specific network segments or host identifiers.
- Scheduled network discovery tasks that are part of IT operations can mimic port scanning behavior. Document and exclude these tasks by setting up time-based exceptions or identifying their unique process signatures.

### Response and remediation

- Isolate the compromised host from the network immediately to prevent further scanning and potential lateral movement.
- Terminate any suspicious processes identified by the process.executable field to halt ongoing malicious activities.
- Conduct a thorough review of the compromised host's system logs and network traffic to identify any unauthorized access or data exfiltration attempts.
- Patch and update all software and services on the compromised host to close any vulnerabilities that may have been exploited.
- Change all credentials associated with the compromised host and any potentially affected systems to prevent unauthorized access.
- Monitor the network for any further signs of scanning activity or other suspicious behavior from other hosts, indicating potential additional compromises.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.

