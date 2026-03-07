---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual DNS Activity" prebuilt detection rule.'
---

# Unusual DNS Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual DNS Activity
DNS is crucial for translating domain names into IP addresses, enabling network communication. Adversaries exploit DNS by using rare domains for malicious activities like phishing or command-and-control. The 'Unusual DNS Activity' detection rule leverages machine learning to identify atypical DNS queries, signaling potential threats such as unauthorized access or data exfiltration.

### Possible investigation steps

- Review the DNS query logs to identify the specific rare domain that triggered the alert and determine its reputation using threat intelligence sources.
- Analyze the source IP address associated with the unusual DNS query to identify the device or user responsible for the activity.
- Check for any recent changes or anomalies in the network activity of the identified device or user, such as unusual login times or access to sensitive data.
- Investigate any related alerts or logs that might indicate a broader pattern of suspicious activity, such as multiple rare domain queries or connections to known malicious IP addresses.
- Examine endpoint security logs on the affected device for signs of malware or unauthorized software that could be responsible for the unusual DNS activity.
- Assess whether the unusual DNS activity aligns with known tactics, techniques, and procedures (TTPs) associated with command-and-control or data exfiltration, referencing the MITRE ATT&CK framework for guidance.

### False positive analysis

- Legitimate software updates may trigger unusual DNS queries as they contact uncommon domains for downloading updates. Users can create exceptions for known update servers to reduce false positives.
- Internal applications using dynamic DNS services might generate rare DNS queries. Identifying and whitelisting these services can help in minimizing false alerts.
- Third-party security tools or monitoring solutions may use unique DNS queries for their operations. Verify and exclude these tools from the detection rule to prevent unnecessary alerts.
- Cloud services often use diverse and uncommon domains for legitimate operations. Regularly review and update the list of trusted cloud service domains to avoid false positives.
- New or infrequently accessed legitimate websites may appear as unusual. Users should monitor and whitelist these domains if they are confirmed to be safe and necessary for business operations.

### Response and remediation

- Isolate the affected system from the network to prevent further communication with the suspicious DNS domain and potential data exfiltration.
- Conduct a thorough scan of the isolated system using updated antivirus and anti-malware tools to identify and remove any malicious software.
- Review and block the identified unusual DNS domain at the network perimeter to prevent other systems from communicating with it.
- Analyze logs and network traffic to identify any other systems that may have communicated with the same unusual DNS domain and apply similar containment measures.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are compromised.
- Restore the affected system from a known good backup if malware removal is not possible or if system integrity is in question.
- Update and enhance DNS monitoring rules to detect similar unusual DNS activity in the future, ensuring rapid identification and response to potential threats.
